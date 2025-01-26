import React from 'react';
import { ArrowRight, ArrowLeft } from 'lucide-react';

type CategoryPreviewData = {
  [key: string]: {
    title: string;
    gradient: string;
    items: Array<{
      name: string;
      price: number;
      description: string;
      image: string;
    }>;
  };
};

const CATEGORY_PREVIEW: CategoryPreviewData = {
  airlines: {
    title: "Flight Tickets",
    gradient: "from-blue-500 to-indigo-600",
    items: [
      {
        name: "NYC → LDN",
        price: 2499.99,
        description: "Business Class, Emirates",
        image: "/api/placeholder/60/60"
      },
      {
        name: "LAX → TYO",
        price: 3299.99,
        description: "First Class, ANA",
        image: "/api/placeholder/60/60"
      }
    ]
  },
  grocery: {
    title: "Whole Foods",
    gradient: "from-green-500 to-emerald-600",
    items: [
      {
        name: "Fresh Produce Bundle",
        price: 89.99,
        description: "Organic Selection",
        image: "/api/placeholder/60/60"
      },
      {
        name: "Premium Dairy",
        price: 45.50,
        description: "Farm Fresh",
        image: "/api/placeholder/60/60"
      }
    ]
  },
  bigticket: {
    title: "Apple Store",
    gradient: "from-purple-500 to-indigo-500",
    items: [
      {
        name: "iPhone 15 Pro Max",
        price: 1299.99,
        description: "256GB Titanium",
        image: "/api/placeholder/60/60"
      },
      {
        name: "MacBook Pro",
        price: 2499.99,
        description: "14-inch M3 Pro",
        image: "/api/placeholder/60/60"
      }
    ]
  },
dining: {
    title: "Fine Dining",
    gradient: "from-red-500 to-pink-600",
    items: [
        {
            name: "Gourmet Dinner",
            price: 199.99,
            description: "5-course meal at a Michelin-star restaurant",
            image: "/api/placeholder/60/60"
        },
        {
            name: "Wine Tasting",
            price: 89.99,
            description: "Selection of premium wines",
            image: "/api/placeholder/60/60"
        }
    ]
}
};

type CheckoutPreviewProps = {
  categoryId: string;
  onBack: () => void;
  onProceedToPayment: (amount: number) => void;
};

const CheckoutPreview = ({ categoryId, onBack, onProceedToPayment }: CheckoutPreviewProps) => {
  const category = CATEGORY_PREVIEW[categoryId];
  const total = category.items.reduce((sum, item) => sum + item.price, 0);

  return (
    <div className="h-full bg-white">
      <div className={`h-64 bg-gradient-to-r ${category.gradient} relative`}>
        <button 
          onClick={onBack}
          className="absolute top-4 left-4 w-10 h-10 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm"
        >
          <ArrowLeft className="w-6 h-6 text-white" />
        </button>
        
        <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
          <h2 className="text-2xl font-bold mb-1">{category.title}</h2>
          <p className="opacity-90">Order Preview</p>
        </div>
      </div>

      <div className="p-6 -mt-6 rounded-t-3xl bg-white relative">
        <div className="space-y-6">
          {category.items.map((item, index) => (
            <div key={index} className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gray-100 rounded-xl flex items-center justify-center">
                <img 
                  src={item.image} 
                  alt={item.name}
                  className="w-12 h-12 rounded-lg object-cover"
                />
              </div>
              <div className="flex-1">
                <h3 className="font-medium">{item.name}</h3>
                <p className="text-sm text-gray-500">{item.description}</p>
              </div>
              <p className="font-medium">${item.price.toFixed(2)}</p>
            </div>
          ))}

          <div className="pt-6 border-t space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-500">Subtotal</span>
              <span className="font-medium">${total.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Tax</span>
              <span className="font-medium">Included</span>
            </div>
            <div className="flex justify-between pt-3 border-t">
              <span className="font-medium">Total to Pay</span>
              <span className="font-bold text-xl">${total.toFixed(2)}</span>
            </div>
          </div>

          <button
            onClick={() => onProceedToPayment(total)}
            className="w-full bg-blue-500 text-white py-4 rounded-xl font-medium transform transition-all duration-200 hover:bg-blue-600 active:scale-[0.98] flex items-center justify-center gap-2"
          >
            <span>Continue to Payment</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default CheckoutPreview;