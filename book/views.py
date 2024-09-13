from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
# method_decorator
from django.utils.decorators import method_decorator
from django.contrib import messages
from PyPDF2 import PdfFileReader, PdfFileWriter
import os


# Create your views here.

# @login_required
def home(request):
    books_list = Book.objects.all()
    paginator = Paginator(books_list, 20)  # Show 5 books per page

    page_number = request.GET.get('page')  # Get the page number from the request
    books = paginator.get_page(page_number)  # Get books for the selected page

    context = {'books': books}

    return render(request, 'home.html', context)

@login_required
def donate_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        # author = Author.objects.get_or_create(name=author)
        

        genre = request.POST.get('genre')
        publish_year = request.POST.get('publish_year')
        summary = request.POST.get('summary')
        cover = request.FILES.get('cover')
                        
        cover.name = title + '.jpg'
        pdf = request.FILES.get('pdf')
        # change the name of the file to the title of the book
        pdf.name = title + '.pdf'
        

        donar = request.user

        book = Book(title=title, author=author, genre=genre, publish_year=publish_year, summary=summary, cover=cover, pdf=pdf, donar=donar)
        book.save()
        messages.success(request, 'Book added successfully')
        return redirect('donate_book')
    return render(request, 'donate_book.html')

@method_decorator(login_required, name='dispatch')
class BookDetailView(TemplateView):
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('pk')
        book = Book.objects.get(pk=book_id)
        context['book'] = book
        return context 


@login_required
def book_download(request, pk):
    book = Book.objects.get(pk=pk)
    book.pdf.url
    response = redirect(book.pdf.url)
    response['Content-Disposition'] = 'attachment'
    return response

    

@method_decorator(login_required, name='dispatch')
class MyDonations(TemplateView):
    template_name = 'my_donations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        donar = self.request.user
        books_list = Book.objects.filter(donar=donar)
        
        # Pagination logic
        paginator = Paginator(books_list, 5)  # Show 5 books per page
        page = self.request.GET.get('page')

        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)  # If page is not an integer, show the first page
        except EmptyPage:
            books = paginator.page(paginator.num_pages)  # If page is out of range, show the last page
        
        context['books'] = books
        
        return context

# class MyDonations(TemplateView):
#     template_name = 'my_donations.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         donar = self.request.user
#         books = Book.objects.filter(donar=donar)
#         context['books'] = books
#         return context


@login_required
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    # delete the book file
    book.pdf.delete()


    book.delete()

    messages.success(request, 'Book deleted successfully')
    return redirect('home')


@login_required
def update_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        publish_year = request.POST.get('publish_year')
        summary = request.POST.get('summary')
        cover = request.FILES.get('cover')
        cover.name = title + '.jpg'
        pdf = request.FILES.get('pdf')
        pdf.name = title + '.pdf'
        book.title = title
        book.author = author
        book.genre = genre
        book.publish_year = publish_year
        book.summary = summary
        book.cover = cover
        book.pdf = pdf
        book.save()
        messages.success(request, 'Book updated successfully')
        return redirect('home')
    return render(request, 'update_book.html', {'book': book})

# search view
def search(request):
    query = request.GET.get('query')
    books = Book.objects.filter(title__icontains=query)
    context = {'books': books}
    return render(request, 'search.html', context)


# convert epub to pdf
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, Http404
# from .forms import FileUploadForm
from django.conf import settings
from fpdf import FPDF
from docx import Document
from PIL import Image
from ebooklib import epub
from bs4 import BeautifulSoup
import shutil

# Function to convert epub to pdf
import os
import zipfile
import pdfkit
from ebooklib import epub
from bs4 import BeautifulSoup
import tempfile

def convert_epub_to_pdf(epub_path, output_pdf):
    # Read the EPUB file
    book = epub.read_epub(epub_path)

    # Create a temporary directory to store extracted HTML and images
    with tempfile.TemporaryDirectory() as temp_dir:
        html_files = []
        
        # Extract all HTML and images
        for item in book.get_items():
            if isinstance(item, epub.EpubHtml):
                soup = BeautifulSoup(item.content, 'html.parser')
                
                # Save HTML content into a file in the temporary directory
                html_file_path = os.path.join(temp_dir, f'{item.get_name()}.html')
                with open(html_file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                html_files.append(html_file_path)
            
            # Save images to the temp directory
            elif item.media_type.startswith('image/'):
                image_file_path = os.path.join(temp_dir, item.get_name())
                with open(image_file_path, 'wb') as img_file:
                    img_file.write(item.get_content())

        # Concatenate all the HTML files into one if there are multiple
        combined_html_file = os.path.join(temp_dir, 'combined.html')
        with open(combined_html_file, 'w', encoding='utf-8') as combined_file:
            for html_file in html_files:
                with open(html_file, 'r', encoding='utf-8') as f:
                    combined_file.write(f.read())
                    combined_file.write('<div style="page-break-after: always;"></div>')  # Add page breaks between chapters

        # Convert the combined HTML file into PDF using pdfkit
        pdfkit.from_file(combined_html_file, output_pdf)

    print(f'EPUB converted to PDF: {output_pdf}')




# Convert various file types to PDF
def convert_to_pdf(file_path, file_name):
    extension = os.path.splitext(file_name)[1].lower()
    output_pdf = os.path.join(settings.MEDIA_ROOT, 'converted', f'{os.path.splitext(file_name)[0]}.pdf')

    if extension == '.txt':
        # Convert text file to PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        with open(file_path, 'r') as file:
            for line in file:
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, line)
        pdf.output(output_pdf)
    elif extension == '.docx':
        # Convert DOCX to PDF
        doc = Document(file_path)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for para in doc.paragraphs:
            pdf.multi_cell(0, 10, para.text)
        pdf.output(output_pdf)
    elif extension in ['.jpg', '.jpeg', '.png']:
        # Convert image to PDF
        image = Image.open(file_path)
        pdf = FPDF()
        pdf.add_page()
        pdf.image(file_path, x=10, y=10, w=190)
        pdf.output(output_pdf)
    elif extension == '.epub':
        # Convert EPUB to PDF
        convert_epub_to_pdf(file_path, output_pdf)
    else:
        raise ValueError("Unsupported file format")
    
    return output_pdf



def convert_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        
        try:
            output_pdf = convert_to_pdf(file_path, file.name)
        except ValueError as e:
            return HttpResponse(f"Error: {e}")
        
        return FileResponse(open(output_pdf, 'rb'))
    
    return render(request, 'converter.html')








