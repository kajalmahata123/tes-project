import { LucideIcon } from 'lucide-react';

export type CategoryId = 'grocery' | 'airlines' | 'bigticket' | 'dining';

export type Category = {
  id: CategoryId;
  name: string;
  icon: LucideIcon;
  gradient: string;
  offers: number;
  description: string;
  metrics: {
    growth: string;
    engagement: string;
  };
};

export type Merchant = {
  id: number;
  name: string;
  category: string;
  offer: string;
  image: string;
  gradient: string;
  tag: string;
  metrics: {
    satisfaction: string;
    users: string;
  };
};

export type ViewType = 'home' | 'preview' | 'payment';

export type CategoryItem = {
  id: number;
  name: string;
  price: number;
  description: string;
  quantity: number;
};

export type CategoryData = {
  name: string;
  gradient: string;
  logo: string;
  items: CategoryItem[];
};

export type CategoryCheckoutData = {
  [K in CategoryId]: CategoryData;
};


