import React, { useState } from 'react';
import { 
  CreditCard, Shield, DollarSign, Calendar,
  ChevronRight, Tag, X, Battery, Signal, Wifi, Check
} from 'lucide-react';

type ViewType = 'main' | 'details' | 'success';

interface InstallmentPlan {
  months: number;
  interest: number;
  processingFee: number;
  minAmount: number;
  monthlyAmount: number;
  totalAmount: number;
}

interface SpecialOffer {
  type: string;
  description: string;
  validity: string;
}

interface CardBenefits {
  cashback: number | null;
  points: number | null;
  installments: InstallmentPlan[];
  protection: {
    extended_warranty: {
      duration: string;
      coverage: string;
    };
  };
  special_offers: SpecialOffer[];
}

interface Card {
  id: string;
  type: string;
  network: string;
  last4: string;
  isDefault: boolean;
  benefits: CardBenefits;
}

const SAMPLE_DATA = {
  transaction: {
    merchant: {
      name: "Apple Store",
      category: "Electronics",
      special_offers: ["Extra 5% off with selected cards"],
      merchant_type: "Premium Retailer"
    },
    amount: 1299.99,
    date: new Date().toISOString(),
    eligible_for_installments: true
  },
  cards: [
    {
      id: "card_1",
      type: "Rewards Plus",
      network: "Mastercard",
      last4: "4567",
      isDefault: true,
      benefits: {
        cashback: 0.05,
        points: null,
        installments: [
          { 
            months: 3, 
            interest: 0,
            processingFee: 0,
            minAmount: 500,
            monthlyAmount: 433.33,
            totalAmount: 1299.99
          }
        ],
        protection: {
          extended_warranty: {
            duration: "1 year extra",
            coverage: "Doubles manufacturer warranty"
          }
        },
        special_offers: [
          {
            type: "Cashback Bonus",
            description: "Extra 5% on first purchase",
            validity: "30 days"
          }
        ]
      }
    }
  ]
};

const MobileDeviceDemo: React.FC = () => {
  const [selectedCard, setSelectedCard] = useState<string | undefined>(
    SAMPLE_DATA.cards.find(card => card.isDefault)?.id
  );
  const [currentView, setCurrentView] = useState<ViewType>('main');
  const [activeCard, setActiveCard] = useState<Card | null>(null);

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const handleCardClick = (card: Card): void => {
    setSelectedCard(card.id);
    setActiveCard(card);
    setCurrentView('details');
  };

  const handlePaymentClick = (): void => {
    setCurrentView('success');
  };

  const handleBackToMain = (): void => {
    setCurrentView('main');
  };

  const renderCardDetails = (card: Card): JSX.Element => (
    <div className="space-y-4 px-1">
      <div className="p-3 bg-gray-50 rounded-lg">
        <div className="flex items-center text-sm font-medium text-gray-600">
          <DollarSign className="w-4 h-4 mr-1 text-green-500" />
          Rewards Value
        </div>
        <p className="mt-1 text-lg font-semibold">
          {card.benefits.cashback 
            ? formatCurrency(SAMPLE_DATA.transaction.amount * card.benefits.cashback)
            : `${Math.floor(SAMPLE_DATA.transaction.amount * (card.benefits.points || 0))} points`
          }
        </p>
      </div>
      
      {card.benefits.installments.map((plan) => (
        <div key={plan.months} className="p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center mb-2">
            <Calendar className="w-4 h-4 mr-2 text-orange-500" />
            <p className="font-medium">{plan.months} months</p>
          </div>
          <p className="ml-6 font-medium">
            {formatCurrency(plan.monthlyAmount)}/mo
          </p>
        </div>
      ))}

      {card.benefits.special_offers.map((offer, index) => (
        <div key={index} className="p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center mb-2">
            <Tag className="w-4 h-4 mr-2 text-purple-500" />
            <p className="font-medium">{offer.description}</p>
          </div>
          <p className="ml-6 text-sm text-gray-600">
            Valid: {offer.validity}
          </p>
        </div>
      ))}
    </div>
  );

  const renderContent = (): JSX.Element => {
    if (currentView === 'success') {
      return (
        <div className="h-full flex flex-col items-center justify-center px-4">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-6">
            <Check className="w-8 h-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold mb-2">Payment Successful!</h2>
          <button 
            className="mt-8 w-full py-3 px-4 bg-blue-600 text-white rounded-lg"
            onClick={handleBackToMain}
          >
            Back to Home
          </button>
        </div>
      );
    }

    if (currentView === 'details') {
      return (
        <div className="h-full overflow-y-auto">
          <div className="sticky top-0 bg-white border-b">
            <div className="flex items-center p-4">
              <button 
                className="p-2 hover:bg-gray-100 rounded-lg mr-2"
                onClick={handleBackToMain}
              >
                <X className="w-4 h-4" />
              </button>
              <h2 className="font-semibold">{activeCard?.type} Details</h2>
            </div>
          </div>
          <div className="p-4">
            {activeCard && renderCardDetails(activeCard)}
          </div>
        </div>
      );
    }

    return (
      <div className="h-full relative">
        <div className="h-full overflow-y-auto pb-20">
          <div className="p-4 border-b">
            <h3 className="text-lg font-semibold">{SAMPLE_DATA.transaction.merchant.name}</h3>
            <p className="text-2xl font-bold mt-2">
              {formatCurrency(SAMPLE_DATA.transaction.amount)}
            </p>
          </div>

          <div className="p-4">
            <h2 className="text-lg font-semibold mb-4">Select Payment Method</h2>
            <div className="space-y-3">
              {SAMPLE_DATA.cards.map((card) => (
                <div 
                  key={card.id}
                  className={`p-4 border rounded-lg cursor-pointer ${
                    selectedCard === card.id ? 'ring-2 ring-blue-500' : ''
                  }`}
                  onClick={() => handleCardClick(card)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <CreditCard className={`w-5 h-5 ${
                        selectedCard === card.id ? 'text-blue-500' : 'text-gray-400'
                      }`} />
                      <div className="ml-3">
                        <p className="font-medium">{card.type}</p>
                        <p className="text-sm text-gray-600">
                          {card.network} •••• {card.last4}
                        </p>
                      </div>
                    </div>
                    <ChevronRight className="w-5 h-5 text-gray-400" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="absolute bottom-0 inset-x-0 p-4 bg-white border-t">
          <button 
            className="w-full py-3 px-4 bg-blue-600 text-white rounded-lg font-medium"
            onClick={handlePaymentClick}
          >
            Pay {formatCurrency(SAMPLE_DATA.transaction.amount)}
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-[393px] h-[852px] bg-black rounded-[55px] overflow-hidden relative border-8 border-black">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 h-[35px] w-[126px] bg-black rounded-b-[18px] z-50 mt-2">
          <div className="absolute top-[10px] w-[90px] h-[9px] bg-neutral-900 rounded-[18px] left-1/2 -translate-x-1/2" />
          <div className="absolute right-[22px] top-[7px] w-[13px] h-[13px] rounded-full bg-neutral-950" />
        </div>

        <div className="h-full w-full bg-white rounded-[45px] overflow-hidden">
          <div className="h-12 flex items-center justify-between px-6 pt-2">
            <div className="text-sm font-medium">9:41</div>
            <div className="flex items-center space-x-2">
              <Signal className="w-4 h-4" />
              <Wifi className="w-4 h-4" />
              <Battery className="w-4 h-4" />
            </div>
          </div>

          <div className="relative h-[calc(100%-3rem)]">
            {renderContent()}
            <div className="absolute bottom-1 left-1/2 -translate-x-1/2 w-[134px] h-[5px] bg-neutral-200 rounded-full" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default MobileDeviceDemo;
