from flask import render_template, redirect
from flask.views import MethodView

from db import db


class FormView(MethodView):
    form_class = None
    template_name = ''
    success_url = ''

    def perform_post(self, form, **kwargs):
        pass

    def get_form(self, **kwargs):
        return self.form_class()

    def get_context(self, **kwargs):
        return {'form': kwargs.get('form')}

    def get(self, **kwargs):
        form = self.get_form(**kwargs)
        context = self.get_context(form=form, **kwargs)
        return render_template(self.template_name, **context)

    def post(self, **kwargs):
        form = self.get_form(**kwargs)
        if form.validate_on_submit():
            self.perform_post(form, **kwargs)
            return redirect(next(self.success_url))
        context = self.get_context(form=form, **kwargs)
        return render_template(self.template_name, **context)


class GenericViewMixin:
    entity = None

    def get_collection(self):
        if self.entity is None:
            raise NotImplementedError('No entity was specified for that view.')
        return self.entity.query.filter()

    def get_obj(self, **kwargs):
        collection = self.get_collection()
        return collection.get_or_404(kwargs.get('pk'))


class ListView(MethodView, GenericViewMixin):
    template_name = ''

    def get(self):
        collection = self.get_collection()
        return render_template(self.template_name, objects=collection)


class RetrieveView(MethodView, GenericViewMixin):
    template_name = ''

    def get(self, pk):
        obj = self.get_obj(pk=pk)
        return render_template(self.template_name, obj=obj)


class CreateView(FormView, GenericViewMixin):
    template_name = ''
    success_url = ''

    def perform_post(self, form, **kwargs):
        entity = self.entity
        if self.entity is None:
            entity = self.get_collection()._primary_entity.type
        obj = entity()
        form.populate_obj(obj)
        db.session.add(obj)
        db.session.commit()


class UpdateView(FormView, GenericViewMixin):
    template_name = ''
    success_url = ''

    def get_form(self, **kwargs):
        obj = self.get_obj(**kwargs)
        return self.form_class(obj=obj)

    def get_context(self, **kwargs):
        obj = self.get_obj(**kwargs)
        return {**kwargs, 'obj': obj}

    def perform_post(self, form, **kwargs):
        obj = self.get_obj(**kwargs)
        form.populate_obj(obj)
        db.session.commit()


class DeleteView(MethodView, GenericViewMixin):
    success_url = ''

    def post(self, pk):
        obj = self.get_obj(pk=pk)
        db.session.delete(obj)
        db.session.commit()
        return redirect(next(self.success_url))
