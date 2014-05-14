#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.http import Http404
from sortable_listview import SortableListView

class BaseView(View):
  template_name=None
  model=None
  view_data={}
  where={}
  order_by=[]
  back_url=None
  item_for_page=None
  page_view=None
  default_page_number=1
  footer_value=None #Napisać na to template_context_processor
    
  def get(self, request, *args, **kwargs):
    page = None
    if 'page' in kwargs and kwargs['page'] != u'':
      page = int(kwargs['page'])
    data=[]
    if self.model and self.model is not None:
      try:
        order_by=[]
        if 'sort' in kwargs and kwargs['sort']!='':
          order_by.append(kwargs['sort'])
        if 'where' in kwargs and kwargs['where']!='':
          self.where.update(kwargs['where'])
        if len(self.order_by)>0:
          order_by.extend(self.order_by)
        if len(self.where)>0 and len(order_by)>0:
          data = self.model.objects.filter(**self.where).order_by(*order_by)
        elif len(self.where)>0:
          data = self.model.objects.filter(**self.where)
        elif len(order_by)>0:
          data = self.model.objects.all().order_by(*order_by)
        else:
          data = self.model.objects.all()
      except:
        return render(request, 'info.html', {'back_url':self.back_url, 'errors':[_(u'Błąd w klasie BaseView.'), ]})
    paginator = Paginator(data, self.item_for_page)
    if page and paginator.num_pages >= page:
      data = paginator.page(page)
    elif paginator.num_pages >= self.default_page_number:
      data = paginator.page(self.default_page_number)
    else:
      raise Http404()
    self.view_data.update({'page':page, 'paginator':paginator, 'data':data, 'page_view':self.page_view, 'footer_value':self.footer_value,'request':request})


class BasePaginatedView(SortableListView):
    sort_column_order = None
    paginate_by = 10
    sort_parameter = ''
    
    def get_context_data(self, **kwargs):
        context = super(UserBlogIndex, self).get_context_data(**kwargs)
        if len(self.sort_column_order) != len(self.allowed_sort_fields.keys()):
            raise Error("Długość listy sortowania nie zgadza się z długoścą listy kolumn.")
        if self.sort_column_order != None:
            for item in self.sort_column_order:
                for ddict in context['sort_link_list']:
                    if ddict['attrs'] == item:
                        index = self.sort_column_order.index(item)
                        context['sort_link_list'].remove(ddict)
                        context['sort_link_list'].insert(index, ddict)
                        break
                    elif ddict == context['sort_link_list'][-1]:
                        context['sort_link_list'].append(ddict)
        return context    