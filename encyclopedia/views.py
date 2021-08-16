#import
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages #biblioteca para tratamento de menssagens

from django import forms
from django.forms import TextInput #Ajudar a mudar o tamanho da caixa de texto do formulário

from . import util
import random
import markdown2

mark = markdown2.Markdown()


class NewTitleForm(forms.Form):
    # O Widget é uma representação do Django de um elemento input do HTML
    # no forms do Django alguns elementos já tem o widget padrão. Por exemplo:
    # forms.CharField() já o widget TextInput como padrão, o que se fosse em HTML
    # seria <input type="text"... em Django é:
    # forms.CharField() que é a mesma coisa que forms.CharField(widget=TextInput())
    title = forms.CharField(label=False, max_length=50,
            widget=forms.TextInput(attrs={'size':'19','placeholder':'Buscar'}))

class NewPageForm(forms.Form):
    page_title = forms.CharField(label="Título da Página:")
    content = forms.CharField(label="Conteúdo da Página:", 
    widget=forms.Textarea(attrs={'style':'height:200px;width:900px'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewTitleForm()
    })

def entrypage(request, title):
    # converte o arquivo .md em html
    # OBS no template tem que colocar "|safe" após a variável title_body
    html = mark.convert(util.get_entry(title))
    return render(request, "encyclopedia/entrypage.html", {
        "html": html,
        "title_body": util.get_entry(title),
        "title":title,
        "form": NewTitleForm()
    })

def search(request):

    # Falta fazer com que va direto para a pagina do titulo casa ele exista
    
    # --Se o método for POST
    if request.method == "POST":
        # Carrego o formulário na variável form com os dados de requisição
        form = NewTitleForm(request.POST)
        # verifico se o formulário é válido

        if form.is_valid():
            # pega o dado digitado no formulario e armazena em newtitle
            newtitle = form.cleaned_data['title']
            # pega a lista de todos os titulos que estão em 'entries'
            title = util.list_entries()
            # converte todos os caracteres da lista 'title' em minusculo e salva em titlelower
            titlelower = [x.lower() for x in title]

            # se o que foi pesquisado estiver na lista vai direto para a pagina
            if newtitle.lower() in titlelower:
                return HttpResponseRedirect(reverse("entrypage",args=(newtitle,)))
            # senão vai para uma página de busca
            else:
                return render(request, "encyclopedia/search.html", {
                    "title": titlelower,
                    "newtitle": newtitle.lower(),
                    "form": NewTitleForm()
                })

        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })

    # --Se for uma solicitação GET
    else:
        return render(request, "encyclopedia/search.html", {
            "form": NewTitleForm()
        })

def newpage(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            page_title = form.cleaned_data['page_title']
            content = form.cleaned_data['content']
            title = util.list_entries()
            #quando for salvar a página se o titulo já existir vai dar erro
            if page_title in title:
                #para enviar menssagem de erro, não precisa de uma variável e
                #não precisa passar pro contexto
                messages.error(request, "Erro: Esse título já existe")
                return render(request, "encyclopedia/newpage.html",{
                    "form": NewTitleForm(),
                    "newpage": NewPageForm(),
                    "page_title": page_title,
                })
            #se o título não existir vai salvar na lista e depois abrir a página
            else:
                util.save_entry(page_title, content)
                #prestar atenção do argumento do reverse()
                return HttpResponseRedirect(reverse("entrypage", args=(page_title,)))

    return render(request, "encyclopedia/newpage.html",{
        "form": NewTitleForm(),
        "newpage": NewPageForm()
    })

def editpage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        return render(request, "encyclopedia/editpage.html",{
            'form': NewTitleForm(),
            'title': title,
            'body': body,
        })
    return render(request, "encyclopedia/editpage.html")

def editsave(request):
    #criei essa função para salvar o conteúdo da pagina de edição
    #Fiz com formulário HTML
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
        util.save_entry(title, body)
        #prestar atenção no argumento de reverse() args=(xxx,) tem que ter a virgula
        return HttpResponseRedirect(reverse("entrypage", args=(title,)))

def randompage(request):
    all_pages = util.list_entries()
    rand = random.choice(all_pages)
    return HttpResponseRedirect(reverse("entrypage", args=(rand,)))
