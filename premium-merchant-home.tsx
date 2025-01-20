import React, { useState } from 'react';
import { 
  Battery, Signal, Wifi,
  ShoppingBag, Utensils, Plane, Car,
  Smartphone, Building2, HeartPulse, GraduationCap,
  Search, ArrowRight, CircleEllipsis, Bell,
  Ticket, ShoppingCart, BanknoteIcon, MapPin
} from 'lucide-react';

interface Category {
  id: string;
  name: string;
  icon: typeof Plane | typeof ShoppingCart | typeof BanknoteIcon | typeof Utensils;
  gradient: string;
  offers: number;
  description: string;
}

interface Merchant {
  id: number;
  name: string;
  category: string;
  offer: string;
  image: string;
  backgroundColor: string;
  badgeColor: string;
  tag: string;
}

interface AirlineDeal {
  id: number;
  name: string;
  route: string;
  offer: string;
  validTill: string;
  points: string;
  image: string;
}

const CATEGORIES: Category[] = [
  {
    id: 'airlines',
    name: 'Airlines',
    icon: Plane,
    gradient: 'from-blue-500 to-indigo-600',
    offers: 15,
    description: 'Flight tickets & rewards'
  },
  {
    id: 'grocery',
    name: 'Grocery',
    icon: ShoppingCart,
    gradient: 'from-green-500 to-emerald-600',
    offers: 18,
    description: 'Supermarkets & stores'
  },
  {
    id: 'bigticket',
    name: 'Big Ticket',
    icon: BanknoteIcon,
    gradient: 'from-purple-500 to-indigo-500',
    offers: 8,
    description: 'Luxury & high-value items'
  },
  {
    id: 'dining',
    name: 'Dining',
    icon: Utensils,
    gradient: 'from-orange-500 to-red-500',
    offers: 12,
    description: 'Restaurants & cafes'
  }
];

const FEATURED_MERCHANTS: Merchant[] = [
  {
    id: 1,
    name: 'Emirates',
    category: 'Airlines',
    offer: 'Up to $400 off + 5x points',
    image: '/api/placeholder/80/80',
    backgroundColor: 'bg-red-50',
    badgeColor: 'bg-red-500',
    tag: 'Premium Partner'
  },
  {
    id: 2,
    name: 'Whole Foods',
    category: 'Grocery',
    offer: '10% cashback + free delivery',
    image: '/api/placeholder/80/80',
    backgroundColor: 'bg-green-50',
    badgeColor: 'bg-green-500',
    tag: 'Grocery Partner'
  },
  {
    id: 3,
    name: 'Best Buy',
    category: 'Big Ticket',
    offer: '24 months no interest',
    image: '/api/placeholder/80/80',
    backgroundColor: 'bg-blue-50',
    badgeColor: 'bg-blue-500',
    tag: 'Electronics'
  }
];

const AIRLINE_DEALS: AirlineDeal[] = [
  {
    id: 1,
    name: 'Delta Airlines',
    route: 'NYC → LAX',
    offer: 'Business from $599',
    validTill: '2 days left',
    points: '3x points',
    image: '/api/placeholder/60/60'
  },
  {
    id: 2,
    name: 'United Airlines',
    route: 'CHI → MIA',
    offer: 'Economy from $299',
    validTill: '5 days left',
    points: '2x points',
    image: '/api/placeholder/60/60'
  }
];

type TabType = 'featured' | 'trending';

const CategoryCard: React.FC<{ category: Category }> = ({ category }) => {
  const { icon: Icon } = category;
  
  return (
    <button
      className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-gray-50 to-white p-5 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 border border-gray-100"
    >
      <div className="relative z-10 flex flex-col items-center text-center">
        <div className={`w-14 h-14 bg-gradient-to-br ${category.gradient} rounded-2xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
          <Icon className="w-7 h-7 text-white" />
        </div>
        
        <div className="space-y-2 w-full">
          <h3 className="text-xl font-bold text-gray-900">{category.name}</h3>
          <p className="text-sm text-gray-600 line-clamp-2">{category.description}</p>
          
          <div className="inline-flex items-center px-3 py-1 rounded-full bg-gray-900/5 text-gray-700">
            <span className="text-sm font-medium">{category.offers} offers</span>
          </div>
        </div>

        <div className="absolute bottom-5 right-5 opacity-0 transform translate-x-5 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-300">
          <div className="w-8 h-8 bg-gray-900 rounded-full flex items-center justify-center">
            <ArrowRight className="w-4 h-4 text-white" />
          </div>
        </div>
      </div>

      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-gray-900/[0.02] to-transparent rounded-full transform translate-x-16 -translate-y-8" />
      <div className="absolute bottom-0 left-0 w-16 h-16 bg-gradient-to-tr from-gray-900/[0.02] to-transparent rounded-full transform -translate-x-8 translate-y-8" />
    </button>
  );
};

const MerchantCard: React.FC<{ merchant: Merchant }> = ({ merchant }) => {
  return (
    <div className="flex items-center p-4 bg-white rounded-xl border shadow-sm hover:shadow-md transition-shadow">
      <div className={`w-16 h-16 ${merchant.backgroundColor} rounded-xl flex items-center justify-center`}>
        <img 
          src={merchant.image} 
          alt={merchant.name}
          className="w-12 h-12 rounded-lg object-cover"
        />
      </div>
      <div className="ml-4 flex-1">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="font-semibold">{merchant.name}</h3>
            <p className="text-sm text-gray-500">{merchant.category}</p>
          </div>
          <div className={`${merchant.badgeColor} text-white text-xs font-medium px-2 py-1 rounded-full`}>
            {merchant.tag}
          </div>
        </div>
        <div className="mt-1 flex items-center">
          <span className="text-sm font-medium text-green-600">{merchant.offer}</span>
          <ArrowRight className="w-4 h-4 text-gray-400 ml-1" />
        </div>
      </div>
    </div>
  );
};

const HomePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('featured');

  const handleTabChange = (tab: TabType) => {
    setActiveTab(tab);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      {/* Device Frame */}
      <div className="w-[393px] h-[852px] bg-black rounded-[55px] shadow-xl overflow-hidden relative border-8 border-black">
        {/* Dynamic Island */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 h-[35px] w-[126px] bg-black rounded-b-[18px] z-50 mt-2">
          <div className="absolute top-[10px] w-[90px] h-[9px] bg-neutral-900 rounded-[18px] left-1/2 -translate-x-1/2" />
          <div className="absolute right-[22px] top-[7px] w-[13px] h-[13px] rounded-full bg-neutral-950" />
        </div>

        {/* Screen Content */}
        <div className="h-full w-full bg-white rounded-[45px] overflow-hidden">
          {/* Status Bar */}
          <div className="h-12 bg-white flex items-center justify-between px-6 pt-2">
            <div className="text-sm font-medium">9:41</div>
            <div className="flex items-center space-x-2">
              <Signal className="w-4 h-4" />
              <Wifi className="w-4 h-4" />
              <Battery className="w-4 h-4" />
            </div>
          </div>

          {/* Main Content */}
          <div className="relative h-[calc(100%-3rem)]">
            <div className="h-full overflow-y-auto">
              {/* Categories Section */}
              <div className="px-4 py-6">
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h2 className="text-xl font-semibold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                      Premium Categories
                    </h2>
                    <p className="text-sm text-gray-500 mt-1">Explore exclusive rewards & offers</p>
                  </div>
                  <button className="px-4 py-2 rounded-lg bg-gray-900 text-white text-sm font-medium hover:bg-gray-800 transition-colors">
                    View All
                  </button>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  {CATEGORIES.map(category => (
                    <CategoryCard key={category.id} category={category} />
                  ))}
                </div>

                {/* Featured Merchants */}
                <div className="mt-6 space-y-3">
                  {FEATURED_MERCHANTS.map(merchant => (
                    <MerchantCard key={merchant.id} merchant={merchant} />
                  ))}
                </div>
              </div>
            </div>

            {/* Home Indicator */}
            <div className="absolute bottom-1 left-1/2 -translate-x-1/2 w-[134px] h-[5px] bg-neutral-200 rounded-full" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
