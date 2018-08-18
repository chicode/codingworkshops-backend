import graphene

from graphene_django.types import DjangoObjectType

from .models import Workshop


class WorkshopType(DjangoObjectType):
    class Meta:
        model = Workshop


class Query(graphene.ObjectType):
    all_workshops = graphene.List(WorkshopType)
    workshop = graphene.Field(WorkshopType, name=graphene.String(required=True))

    def resolve_all_workshops(self, info, **kwargs):
        return Workshop.objects.all()

    def resolve_workshop(self, info, **kwargs):
        return Workshop.objects.get(name=kwargs.get('name'))



class CreateWorkshopInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)

class CreateWorkshop(graphene.Mutation):
    class Arguments:
        input = CreateWorkshopInput(required=True)

    Output = WorkshopType

    def mutate(self, info, input):
        return Workshop.objects.create(name=input.name, description=input.description)


class Mutation(graphene.ObjectType):
    create_workshop = CreateWorkshop.Field()
