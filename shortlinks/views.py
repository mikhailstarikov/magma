from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShortLink
from .forms import ShortLinkForm


@login_required
def create_short_link(request):
    """Создание короткой ссылки"""
    if request.method == "POST":
        form = ShortLinkForm(request.POST)
        if form.is_valid():
            short_link = form.save(commit=False)
            short_link.created_by = request.user
            short_link.save()
            return redirect("shortlinks:link_detail", short_code=short_link.short_code)
    else:
        form = ShortLinkForm()

    return render(request, "shortlinks/create.html", {"form": form})


@login_required
def link_detail(request, short_code):
    """Страница с информацией о короткой ссылке"""
    short_link = get_object_or_404(ShortLink, short_code=short_code)
    return render(request, "shortlinks/detail.html", {"short_link": short_link})


@login_required
def delete_link(request, short_code):
    """Удаление короткой ссылки"""
    short_link = get_object_or_404(
        ShortLink, short_code=short_code, created_by=request.user
    )

    if request.method == "POST":
        short_link.delete()
        messages.success(request, "Ссылка удалена")
        return redirect("shortlinks:my_links")

    return render(request, "shortlinks/delete_confirm.html", {"short_link": short_link})


def redirect_to_original(request, short_code):
    """Редирект на исходный URL"""
    short_link = get_object_or_404(ShortLink, short_code=short_code, is_active=True)
    short_link.clicks += 1
    short_link.save(update_fields=["clicks"])
    return redirect(short_link.original_url)


@login_required
def my_links(request):
    """Список моих ссылок"""
    links = ShortLink.objects.filter(created_by=request.user)
    return render(request, "shortlinks/my_links.html", {"links": links})
