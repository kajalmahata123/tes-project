import React, { useState } from 'react';
import {  CategoryId, ViewType, CategoryData } from './types';
import IphoneFrame from './IphoneFrame';
import MerchantHome from './merchant-home';

import PaymentView from './PaymentView';
import CheckoutPreview from './chekout-preview';
import { CATEGORY_DATA } from './types/category';


const PaymentApp: React.FC = () => {
 const [view, setView] = useState<ViewType>('home');
 const [selectedCategory, setSelectedCategory] = useState<CategoryId | ''>('');
 const [selectedItem, setSelectedItem] = useState<{
   price: number;
   merchant: string;
   category: string;
 } | null>(null);

 const handleCategorySelect = (categoryId: CategoryId): void => {
   setSelectedCategory(categoryId);
   setView('preview');
 };

 const handleProceedToPayment = (total: number): void => {
   if (selectedCategory) {
   //  const categoryData: CategoryData = CATEGORY_DATA[selectedCategory as keyof typeof CATEGORY_DATA];
  // const categoryData = CATEGORY_DATA[selectedCategory];  
  const categoryData = CATEGORY_DATA[selectedCategory as keyof typeof CATEGORY_DATA];

   setSelectedItem({
       price: total,
       merchant: categoryData.name,
       category: selectedCategory
     });
     setView('payment');
   }
 };

 const handleBack = (to: ViewType): void => {
   setView(to);
 };

 return (
   <IphoneFrame>
     {view === 'home' && (
       <MerchantHome onSelectCategory={handleCategorySelect} />
     )}
     {view === 'preview' && selectedCategory && (
       <CheckoutPreview
         categoryId={selectedCategory}
         onBack={() => handleBack('home')}
         onProceedToPayment={handleProceedToPayment}
       />
     )}
     {view === 'payment' && selectedItem && (
       <PaymentView 
         amount={selectedItem.price}
         merchant={selectedItem.merchant}
         category={selectedItem.category}
         onBack={() => handleBack('preview')}
       />
     )}
   </IphoneFrame>
 );
};

export default PaymentApp;