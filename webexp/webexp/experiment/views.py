from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from .models import Participant, Trial, Code, Log

from collections import namedtuple
from math import ceil

import re
import json
import uuid


Frame = namedtuple("Frame", ["template", "function", "context"])

charities = {
    "people_in_need": "Člověk v tísni",
    "red_cross": "Červený kříž"
    }


@never_cache
def manager(request, code = "", page = 0):
    # manager function
    log = Log(code = str(code), page = page, request = request.method)
    log.save()
    try:
        validCode = Code.objects.get(code = str(code)) # pylint: disable=no-member
    except ObjectDoesNotExist:
        return displayError(request, "Zadali jste chybnou adresu.")
    else:
        if not "participantId" in request.session or validCode.code != request.session["participantId"]:
            if validCode.page == len(sequence) - 1:
                return displayError(request, "Experimentu jste se již zúčastnili.")
            elif validCode.page != 0:
                return displayError(request, "Experiment byl ukončen z důvodu neaktivity.")
            elif len(Participant.objects.filter(status = "finished")) >= 300: # pylint: disable=no-member
                return displayError(request, "Tento sběr dat byl již ukončen, brzy vás ale pozveme do dalšího výzkumu.")
            request.session["participantId"] = str(code)
            request.session["context"] = {}
            request.session["taskStarted"] = False
            request.session["activity"] = 0 # just for the session expiry
            request.session.set_expiry(900)
    posted = request.method == 'POST'
    request.session["activity"] += 1
    if posted:
        try:
            participant = Participant.objects.get(participant_id = str(code)) # pylint: disable=no-member
        except ObjectDoesNotExist:
            participant = Participant(participant_id = str(code))
            participant.status = "started"
            participant.save()              
        if page != validCode.page:
            return displayError(request, "Toto není platná akce.")
        if not sequence[validCode.page].function(request):
            # do not proceed to the next frame if returns True
            validCode.page += 1   
            validCode.save()
    else:
        if page != validCode.page:
            if validCode.page == len(sequence) - 1:
                return displayError(request, "Experimentu jste se již zúčastnili.")
            else:
                posted = True
    request.session["context"].update(sequence[validCode.page].context)
    template = loader.get_template('{}.html'.format(sequence[validCode.page].template))
    log.result = "success"
    log.save()
    if sequence[validCode.page].template == "task" and request.session["taskStarted"]:
        return displayError(request, "V experimentu jsme zaznamenali neočekávané chování a musí být proto ukončen.")
    if posted:
        return HttpResponseRedirect(reverse("session", kwargs = {"code": code, "page": validCode.page}))
    elif page == len(sequence) - 1:
        context = request.session["context"]
        end(request)
        return HttpResponse(template.render(context, request))
    else:
        if sequence[validCode.page].template == "task":
            request.session["taskStarted"] = True
        return HttpResponse(template.render(request.session["context"], request))


def charity(request):
    # charity selection
    try:
        participant = Participant.objects.get(participant_id = request.session["participantId"]) # pylint: disable=no-member
        charity = request.POST['charity']
        request.session["context"]["charity"] = charities[charity]
        request.session.modified = True
        participant.charity = charity
        participant.save()
    except Exception:
        pass 


def account(request):
    # bank account information
    try:
        # checking the provided bank account number
        codes = ['0100', '0300', '0600', '0710', '0800', '2010', '2020', '2030', '2060', '2070', '2100', '2200', '2220', '2240', '2250', '2260', '2275', '2600', '2700', '3030', '3050', '3060', '3500', '4000', '4300', '5500', '5800', '6000', '6100', '6200', '6210', '6300', '6700', '6800', '7910', '7940', '7950', '7960', '7970', '7980', '7990', '8030', '8040', '8060', '8090', '8150', '8200', '8215', '8220', '8225', '8230', '8240', '8250', '8255', '8260', '8265', '8270', '8280', '8290', '8291', '8292', '8293', '8294', '8295', '8296', '8297', '8298']
        providedNumber = request.POST['account'].strip().replace(" ", "")
        pattern = re.findall(r'^(?:([0-9]{1,6})-)?([0-9]{2,10})\/([0-9]{4})$', providedNumber)
        if not pattern:
            # email?
            if not re.search(r'[^@]+@[^@]+\.[^@]+', providedNumber):
                raise Exception(f"Zadané číslo {providedNumber} nemá správný formát.")
        else:
            weights = [6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
            prefix = pattern[0][0].rjust(10, "0")
            main = pattern[0][1].rjust(10, "0")
            bank = pattern[0][2]
            checksum = sum([weights[i] * int(prefix[i]) for i in range(len(prefix))])
            if checksum % 11 != 0:
                raise Exception(f"Zadané číslo {providedNumber} je chybné.")
            checksum = sum([weights[i] * int(main[i]) for i in range(len(prefix))])
            if checksum % 11 != 0:
                raise Exception(f"Zadané číslo {providedNumber} je chybné.")
            if bank not in codes:
                raise Exception(f"Kód banky {bank} v zadaném čísle {providedNumber}  je chybný.")
        # adding the number in the database
        participant = Participant.objects.get(participant_id = request.session["participantId"]) # pylint: disable=no-member
        participant.bank_account = providedNumber
        participant.save()
    except Exception as e:  
        request.session["context"]["exception"] = str(e)
        request.session.modified = True
        return True


def task(request):
    # the task itself
    try:
        data = json.loads(request.body.decode("utf-8"))
        practice = data.pop("practice")
        end = data.pop("lastTrial")        
        if not practice:
            if end:
                participant = Participant.objects.get(participant_id = request.session["participantId"]) # pylint: disable=no-member
                participant.reward = data['reward_total']
                participant.charity_reward = data['charity_total']
                participant.save()
                request.session["context"]["charity_absolute"] = int(abs(data['charity_total']) / 10)
                request.session["context"]["charity_total"] = data['charity_total']
                request.session["context"]["reward_total"] = ceil(data['reward_total'] / 10)
                request.session.modified = True
            trial = Trial(participant_id = request.session["participantId"], **data)
            trial.save()
        elif practice and end:
            request.session["taskStarted"] = False
    except Exception:
        pass
    return not end


def end(request):
    participant = Participant.objects.get(participant_id = request.session["participantId"]) # pylint: disable=no-member
    participant.status = "finished"
    participant.save()
    request.session.flush()


def intro(request):
    # frames showing only instructions
    pass


def displayError(request, text):
    localContext = {"error": text}
    template = loader.get_template('error.html')
    return HttpResponse(template.render(localContext, request))    


def handler404(request, exception, template="404.html"):
    response = template.render({}, request)
    response.status_code = 404
    return response


def handler403(request, exception, template="403.html"):
    response = template.render({}, request)
    response.status_code = 403
    return response


def base(request):
    return displayError(request, "Toto není platná adresa.")


def ping(request, code = ""):
    log = Log(code = str(code), page = 99, request = request.method, result = "success")
    log.save()
    return HttpResponse("pong")


@login_required(login_url='/admin/login/')
def delete(request):
    Code.objects.all().delete() # pylint: disable=no-member
    Participant.objects.all().delete() # pylint: disable=no-member
    Trial.objects.all().delete() # pylint: disable=no-member
    Log.objects.all().delete() # pylint: disable=no-member
    return displayError(request, "It is done!")


@login_required(login_url='/admin/login/')
def codes(request, number = 5):
    urls = []
    if number > 10000:
        return displayError(request, "To je moc.")
    for i in range(number): # pylint: disable=unused-variable
        code = uuid.uuid4()
        Code(code = code).save()
        base = request.build_absolute_uri(reverse("base"))
        urls += [f"{base}{code}/"]
    return HttpResponse(loader.get_template("codes.html").render({"urls": urls}, request))   


@login_required(login_url='/admin/login/')
def showData(request, code = ""):
    try:
        Participant.objects.get(participant_id = str(code)) # pylint: disable=no-member
    except ObjectDoesNotExist:
        return displayError(request, "Kód neexistuje.")
    data = Trial.objects.filter(participant_id = str(code)) # pylint: disable=no-member
    if not data:
        return displayError(request, "Nejsou žádná data z experimentu.")
    else:
        fields = [field.name for field in Trial._meta.get_fields()] # pylint: disable=no-member
        content = "\t".join(fields) + "\n" + "\n".join([str(trial) for trial in data])
        return HttpResponse(content, content_type='text/plain')


@login_required(login_url='/admin/login/')
def showParticipants(request):
    participants = Participant.objects.all() # pylint: disable=no-member
    if not participants:
        return displayError(request, "V databázi nejsou data of žádných participantů.")
    else:
        fields = [field.name for field in Participant._meta.get_fields()] # pylint: disable=no-member
        content = "\t".join(fields) + "\n" + "\n".join([str(participant) for participant in participants])
        return HttpResponse(content, content_type='text/plain')


@login_required(login_url='/admin/login/')
def showParticipantLinks(request):
    participants = Participant.objects.all() # pylint: disable=no-member
    urls = []
    if not participants:
        return displayError(request, "V databázi nejsou data of žádných participantů.")
    else:
        for participant in participants:
            base = request.build_absolute_uri(reverse("base"))
            code = participant.participant_id
            urls += [f"{base}data/{code}/"]
        return HttpResponse(loader.get_template("codes.html").render({"urls": urls}, request)) 


@login_required(login_url='/admin/login/')
def downloadCodes(request, filename = "codes"):
    return downloadData(request, Code, filename)

@login_required(login_url='/admin/login/')
def downloadParticipants(request, filename = "participants"):
    return downloadData(request, Participant, filename)

@login_required(login_url='/admin/login/')
def downloadTrials(request, filename = "trials"):
    return downloadData(request, Trial, filename)

@login_required(login_url='/admin/login/')
def downloadLogs(request, filename = "logs"):
    return downloadData(request, Log, filename)

def downloadData(request, table, filename):
    data = table.objects.all() 
    if not data:
        return displayError(request, "V databázi nejsou žádná data.")
    else:
        fields = [field.name for field in table._meta.get_fields()] # pylint: disable=no-member
        content = "\t".join(fields) + "\n" + "\n".join([str(row) for row in data])
        response = HttpResponse(content, content_type="text/plain,charset=utf8")
        response['Content-Disposition'] = 'attachment; filename={0}.txt'.format(filename)
        return response


sequence = [
    Frame("intro", intro, {}),
    Frame("charity", charity, {}),
    Frame("instructions1", intro, {}),
    Frame("instructions2", intro, {}),
    Frame("instructions3", intro, {}),
    Frame("task", task, {"practice": 1}),
    Frame("instructions4", intro, {}),
    Frame("instructions5", intro, {}),
    Frame("instructions6", intro, {}),
    Frame("instructions7", intro, {}),
    Frame("instructions8", intro, {}),
    Frame("task", task, {"practice": 0}),
    Frame("account", account, {}),
    Frame("ending", intro, {})
    ]


