from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, ExercisePlan, NutritionPlan


class ProductListView(ListView):
    """
    Display all products with filtering by type
    """

    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)


        # Filter by product type
        product_type = self.request.GET.get('type')
        if product_type:
            queryset = queryset.filter(product_type=product_type)

        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)


        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = Product.PRODUCT_TYPES
        context['current_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context
    
class ProductDetailView(DetailView):
    """
    Display individual product details
    """

    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()


        # Get product-specific details
        if product.product_type == 'exercise':
            try:
                context['exercise_details'] = product.exercise_details
            except ExercisePlan.DoesNotExist:
                context['exercise_details'] = None
        elif product.product_type == 'nutrition':
            try:
                context['nutrition_details'] = product.nutrition_details
            except NutritionPlan.DoesNotExist:
                context['nutrition_details'] = None


        # Check if user has purchased this product
        if self.request.user.is_authenticated:
            from .models import ProductPurchase
            context['is_purchased'] = ProductPurchase.objects.filter(
                user=self.request.user,
                product=product,
                is_active=True
            ).exists()
        else:
            context['is_purchased'] = False
        
        return context

