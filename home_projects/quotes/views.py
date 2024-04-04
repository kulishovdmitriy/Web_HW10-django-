from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from .forms import AuthorForm, QuoteForm
from .models import Quote, Tag


# Create your views here.
def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def add_author(request):
    if not request.user.is_authenticated:
        return redirect(to='users:signin')
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})


def add_quote(request):
    if not request.user.is_authenticated:
        return redirect(to='users:signin')
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


def top_ten_tags(request):
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    return render(request, 'quotes/top_ten_tags.html', {'top_tags': top_tags})


def quote_detail(request, quote_id):
    quote = Quote.objects.get(pk=quote_id)
    return render(request, 'quotes/quote_detail.html', {'quote': quote})


def quotes_by_tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name__iexact=tag_name)
    all_tags = Tag.objects.all()
    return render(request, 'quotes/index.html', {'quotes': quotes, 'all_tags': all_tags, 'tag_name': tag_name})


def all_quotes(request):
    all_tags = Tag.objects.all()
    return render(request, 'quotes/index.html', {'all_tags': all_tags})
