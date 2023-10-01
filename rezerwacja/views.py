import datetime

from django.shortcuts import render, redirect
from django.views import View

from rezerwacja.models import Room, Reservations


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'base.html')

class AddingNewRoom(View):
    def get(self, request):
        return render(request, 'AddNewRoom.html')
    def post(self, request):
        name = request.POST['name']
        capacity = request.POST['capacity']
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector') == "on"
        if not name:
            return render(request, 'AddNewRoom.html', {"Brak nazwy - podaj nazwę"})
        if capacity < 0:
            return render(request, 'AddNewRoom.html', {"Podawana ilość musi być większa od zera"})
        if Room.objects.filter(name=name).first():
            return render(request, "AddNewRoom.html")

        Room.objects.create(name=name, room_capacity=capacity, projector_availability=projector)
        return redirect('/room/')

class ShowRoom(View):
    def get(self, request):
        rooms = Room.objects.all()
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservations_set.all()]
            room.reserved = datetime.date.today() in reservation_dates
        return render(request, 'ShowRoom.html', context={"rooms":rooms})

class Delete(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        return render(request, 'Delete.html', {'object': room})

    def post(self, request, id):
        odp = request.POST['odp']
        if odp == 'Tak':
            Room.objects.get(pk=id).delete()
        return redirect('/room/')


class Modify(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        return render(request, "Modify.html", context={"room": room})
    def post(self,request, id):
        room = Room.objects.get(pk=id)
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector') == "on"
        if capacity < 1:
            return render(request, "Modify.html", {"room": room, "error:": "Pojemność zbyt mała"})
        if not name:
            return render(request, "Modify.html", {"room": room, "error:": "Brak nazwy"})
        try:
            if name != room.name:
                Room.objects.get(name=name)
                return render(request, "Modify.html", context={"room": room, "error:": "Sala o podanej nazwie istnieje"})
        except Room.DoesNotExist:
            pass
        room.name = name
        room.room_capacity = capacity
        room.projector_availability = projector
        room.save()
        return redirect('/room/')



class RoomReservation(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        return render(request, 'RoomReserve.html', {"room": room})

    def post(self, request,id):
        room = Room.objects.get(pk=id)
        date = request.POST.get('date')
        comment = request.POST.get('comment')
        if Reservations.objects.filter(room_id=room, date=date):
            return render(request, "RoomReserve.html", context={"room": room, "error": "Sala jest już zarezerwowana!"})
        if date < str(datetime.date.today()):
            return render(request, "RoomReserve.html", context={"room": room, "error": "Data jest z przeszłości!"})
        Reservations.objects.create(room_id=room, date=date, comments=comment)
        return redirect('/room/')
class RoomSpecification(View):
    def get(self, request,id):
        room = Room.objects.get(pk=id)
        return render(request, 'RoomSpecification.html', context= {'room': room})
