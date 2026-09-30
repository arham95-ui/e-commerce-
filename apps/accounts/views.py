from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from .forms import RegistrationForm, UserProfileForm, LoginForm
from .models import User, UserProfile
from firebase import FirebaseAuth, FirestoreDB
from datetime import datetime
import uuid

User = get_user_model()

class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('shop:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        
        try:
            # Firebase Auth mein user create karein
            firebase_user = FirebaseAuth.create_user(
                email=user.email,
                password=form.cleaned_data['password1'],
                display_name=f"{user.first_name} {user.last_name}"
            )
            
            if firebase_user:
                # Firestore mein user data save karein
                user_data = {
                    'uid': firebase_user.uid,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'phone': user.phone or '',
                    'address': user.address or '',
                    'city': user.city or '',
                    'state': user.state or '',
                    'country': user.country or 'Pakistan',
                    'zip_code': user.zip_code or '',
                    'is_active': True,
                    'is_email_verified': False,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                FirestoreDB.add_document('users', user_data)
                messages.success(self.request, '✅ Registration successful! Welcome to E-Shop.')
            else:
                messages.warning(self.request, '⚠️ Registration successful but Firebase sync failed.')
        except Exception as e:
            messages.warning(self.request, f'⚠️ Registration successful but Firebase error: {str(e)}')
        
        # Login user
        login(self.request, user)
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Registration failed. Please correct the errors.')
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        
        # Check if user exists in Firebase
        try:
            users = FirestoreDB.query_collection('users', filters=[('email', '==', user.email)])
            if users:
                messages.success(self.request, f'✅ Welcome back, {user.username}!')
            else:
                messages.info(self.request, f'👋 Welcome back, {user.username}!')
        except:
            messages.success(self.request, f'✅ Welcome back, {user.username}!')
        
        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Invalid username or password.')
        return super().form_invalid(form)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, '👋 You have been logged out.')
    return redirect('shop:home')


@login_required
def profile_view(request):
    user = request.user
    
    # Firestore se user data get karein
    try:
        users = FirestoreDB.query_collection('users', filters=[('email', '==', user.email)])
        firestore_user = users[0] if users else None
    except:
        firestore_user = None
    
    context = {
        'user': user,
        'firestore_user': firestore_user
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            
            # Firestore update karein
            try:
                users = FirestoreDB.query_collection('users', filters=[('email', '==', user.email)])
                if users:
                    FirestoreDB.update_document('users', users[0]['id'], {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'phone': user.phone,
                        'address': user.address,
                        'city': user.city,
                        'state': user.state,
                        'country': user.country,
                        'zip_code': user.zip_code,
                        'updated_at': datetime.now().isoformat()
                    })
            except:
                pass
            
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
    
    context = {'form': form}
    return render(request, 'accounts/profile_edit.html', context)