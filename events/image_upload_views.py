from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import os
import uuid
from datetime import datetime
from .models import ImageLibrary

def is_admin_or_organizer(user):
    """Check if user is admin or organizer"""
    if user.is_authenticated:
        if user.is_superuser or user.is_staff:
            return True
        if hasattr(user, 'profile'):
            return 'admin' in user.profile.role or 'organizer' in user.profile.role
    return False

@login_required
@user_passes_test(is_admin_or_organizer)
def image_upload_page(request):
    """Dedicated page for image uploads"""
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title', '')
        category = request.POST.get('category', 'other')
        description = request.POST.get('description', '')
        
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            
            # Generate a unique filename
            filename = f"{uuid.uuid4()}_{image_file.name}"
            
            # Create directory if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'image_library')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save the file
            file_path = os.path.join(upload_dir, filename)
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Create database entry
            relative_path = os.path.join('image_library', filename)
            try:
                new_image = ImageLibrary(
                    title=title,
                    category=category,
                    description=description,
                    image=relative_path,
                    uploaded_by=request.user
                )
                new_image.save()
                messages.success(request, 'Image uploaded successfully!')
            except Exception as e:
                messages.error(request, f'Error saving to database: {str(e)}')
        else:
            messages.error(request, 'No image file provided.')
    
    # Get all images for display
    images = ImageLibrary.objects.all().order_by('-upload_date')
    
    return render(request, 'events/image_upload.html', {
        'images': images,
        'title': 'Image Upload'
    })
