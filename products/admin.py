from django.contrib import admin
from .models import Product, ExercisePlan, NutritionPlan, ProductPurchase
from .models import ProductReview


class ExercisePlanInline(admin.StackedInline):
    model = ExercisePlan
    can_delete = False


class NutritionPlanInline(admin.StackedInline):
    model = NutritionPlan
    can_delete = False

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'is_active', 'created_at')
    list_filter = ('product_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ExercisePlanInline, NutritionPlanInline]

@admin.register(ExercisePlan)
class ExercisePlanAdmin(admin.ModelAdmin):
    list_display = ('product', 'difficulty', 'duration_weeks', 'workouts_per_week')
    list_filter = ('difficulty',)
    search_fields = ('product__name',)


@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ('product', 'meal_type', 'calories_target')
    list_filter = ('meal_type',)
    search_fields = ('product__name',)


@admin.register(ProductPurchase)
class ProductPurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'purchase_date', 'is_active')
    list_filter = ('is_active', 'purchase_date')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('purchase_date',)

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
    readonly_fields = ('created_at', 'updated_at')


