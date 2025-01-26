import React from 'react';
import { Plane, ShoppingCart, CreditCard, Utensils } from 'lucide-react';
import type { Category, CategoryId } from './types';
interface MerchantHomeProps {
  onSelectCategory: (categoryId: CategoryId) => void;
}

const CATEGORIES: Category[] = [
  {
    id: 'airlines',
    name: 'Airlines',
    icon: Plane,
    gradient: 'from-blue-500 to-blue-600',
    offers: 15,
    description: 'Flight tickets & rewards',
    metrics: { growth: '+24%', engagement: '98%' }
  },
  {
    id: 'grocery',
    name: 'Grocery',
    icon: ShoppingCart,
    gradient: 'from-green-500 to-green-600',
    offers: 18,
    description: 'Supermarkets & stores',
    metrics: { growth: '+18%', engagement: '92%' }
  },
  {
    id: 'bigticket',
    name: 'Big Ticket',
    icon: CreditCard,
    gradient: 'from-purple-500 to-purple-600',
    offers: 8,
    description: 'Luxury & high-value items',
    metrics: { growth: '+32%', engagement: '95%' }
  },
  {
    id: 'dining',
    name: 'Dining',
    icon: Utensils,
    gradient: 'from-orange-500 to-orange-600',
    offers: 12,
    description: 'Restaurants & cafes',
    metrics: { growth: '+28%', engagement: '94%' }
  }
];

const CategoryCard: React.FC<{
  category: Category;
  onClick: () => void;
}> = ({ category, onClick }) => {
  const Icon = category.icon;
  
  return (
    <button 
      onClick={onClick}
      className="flex flex-col items-center w-full group"
    >
      <div className={`w-full aspect-square bg-gradient-to-br ${category.gradient} rounded-2xl flex flex-col items-center justify-center p-4 shadow-lg transition-transform group-hover:scale-105`}>
        <Icon className="w-10 h-10 text-white mb-3" />
        <h3 className="text-white text-lg font-semibold mb-1">
          {category.name}
        </h3>
        <p className="text-white/80 text-sm text-center">
          {category.description}
        </p>
        
      </div>
    </button>
  );
};

// Keep existing StatusBar component

const MerchantHome: React.FC<MerchantHomeProps> = ({ onSelectCategory }) => {
  return (
    <div className="bg-gray-50 min-h-screen">
      
      <div className="px-5 pt-4 pb-6">
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <h1 className="text-2xl text-gray-900 font-bold">
              Categories
            </h1>
            <button className="text-blue-600 text-sm font-medium px-4 py-2 rounded-lg bg-blue-50 hover:bg-blue-100 transition-colors">
              View All
            </button>
          </div>
          <p className="text-gray-600 text-sm">
            Select a category to explore rewards & offers
          </p>
        </div>
        
        <div className="grid grid-cols-2 gap-6">
          {CATEGORIES.map(category => (
            <CategoryCard 
              key={category.id}
              category={category}
              onClick={() => onSelectCategory(category.id)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default MerchantHome;