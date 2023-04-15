from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import *
from .serializers import (
    ThreadSerializer, MessageSerializer, MessagePostSerializer,  UserSerializer)
from rest_framework.decorators import action


class ThreadsViewSet(viewsets.GenericViewSet):
    """Threads view set"""
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()

    def list(self, request):
        threads = Thread.objects.all()

        unread_messages = Message.objects.filter(
            thread__in=threads,
            is_read=False,
            recipient=request.user
        )
        # Mark all messages as read after get request with messages
        unread_messages.update(is_read=True)

        serializer = ThreadSerializer(threads, many=True)
        return Response({"data": serializer.data})

    def create(self, request):
        # Retrieve all participants in the thread
        participants = request.data.get("participants", [])
        # Sorf users to check if they already have chat
        participants.sort()

        # Looking for thread with this participants
        threads = Thread.objects.filter(
            participant__in=participants).distinct()

        # Checking process
        for thread in threads:
            thread_participants = list(thread.participant.all())
            # sort to have both lists the same looking
            thread_participants.sort()

            if len(thread_participants) == len(participants):
                # Check if they lists are the same
                if thread_participants == participants:
                    # returning found chat
                    return Response(ThreadSerializer(thread).data, status=200)

        # Chreate new chat
        thread = Thread.objects.create(creater=request.user)
        thread.participant.set(participants)
        return Response(ThreadSerializer(thread).data, status=201)
    # Remove chat

    def destroy(self, request, thread_id):
        thread = Thread.objects.get(id=thread_id)
        thread.delete()
        return Response(status=204)
    # Retrieve list of messages in thread

    @action(detail=True, methods=['get'])
    def get_messages(self, request, pk):
        thread = Thread.objects.get(id=pk)
        messages = thread.message_set.all()
        serializer = MessageSerializer(messages, many=True)
        return Response({"data": serializer.data})


''' Назва класу все сама за себе каже :)'''


class ThreadListByUserAPIView(APIView):
    def get(self, request, user_id):
        threads = Thread.objects.filter(
            creater_id=user_id
        ) | Thread.objects.filter(
            participant=user_id
        )
        serializer = ThreadSerializer(threads, many=True)
        return Response({"data": serializer.data})


class ThreadDetailView(APIView):
    """Info about a thread in detail view"""
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)


class MessageViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = MessagePostSerializer
    queryset = Message.objects.all()

    # Creation of the message process
    def create(self, request):
        serializer = MessagePostSerializer(data=request.data)
        if serializer.is_valid():
            thread_id = serializer.validated_data['thread']
            text = serializer.validated_data['text']
            sender = serializer.validated_data['sender']
            message = Message.objects.create(
                thread_id=thread_id, sender=sender, text=text, is_read=False)
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
