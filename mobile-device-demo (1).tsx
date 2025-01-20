import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  CreditCard, Gift, Shield, Clock, DollarSign, Calendar,
  ChevronRight, Tag, X, Battery, Signal, Wifi, Check
} from 'lucide-react';

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
          },
          { 
            months: 6, 
            interest: 0,
            processingFee: 0,
            minAmount: 1000,
            monthlyAmount: 216.67,
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
    },
    {
      id: "card_2",
      type: "Travel Elite",
      network: "Visa",
      last4: "8901",
      isDefault: false,
      benefits: {
        cashback: null,
        points: 3,
        installments: [
          { 
            months: 3, 
            interest: 0.0899,
            processingFee: 25,
            minAmount: 500,
            monthlyAmount: 449.99,
            totalAmount: 1349.99
          }
        ],
        protection: {
          extended_warranty: {
            duration: "2 years extra",
            coverage: "Triples manufacturer warranty"
          }
        },
        special_offers: [
          {
            type: "Points Bonus",
            description: "3x points on electronics",
            validity: "Ongoing"
          }
        ]
      }
    }
  ]
};

function MobileDeviceDemo() {
  const [selectedCard, setSelectedCard] = useState(SAMPLE_DATA.cards.find(card => card.isDefault)?.id);
  const [currentView, setCurrentView] = useState('main');
  const [activeCard, setActiveCard] = useState(null);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const handleCardClick = (card) => {
    setSelectedCard(card.id);
    setActiveCard(card);
    setCurrentView('details');
  };

  const handlePaymentClick = () => {
    setCurrentView('success');
  };

  const handleBackToMain = () => {
    setCurrentView('main');
  };

  const renderCardDetails = (card) => {
    return (
      <div className="space-y-4 px-1">
        <div className="space-y-3">
          <div className="p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center text-sm font-medium text-gray-600">
              <DollarSign className="w-4 h-4 mr-1 text-green-500" />
              Rewards Value
            </div>
            <p className="mt-1 text-lg font-semibold">
              {card.benefits.cashback 
                ? formatCurrency(SAMPLE_DATA.transaction.amount * card.benefits.cashback)
                : `${Math.floor(SAMPLE_DATA.transaction.amount * card.benefits.points)} points`
              }
            </p>
          </div>
          
          <div className="p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center text-sm font-medium text-gray-600">
              <Shield className="w-4 h-4 mr-1 text-blue-500" />
              Protection
            </div>
            <p className="mt-1 text-sm">
              {card.benefits.protection.extended_warranty.duration} warranty
            </p>
          </div>
        </div>

        <div className="p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center mb-2">
            <Calendar className="w-4 h-4 mr-2 text-orange-500" />
            <p className="font-medium">Available Installments</p>
          </div>
          {card.benefits.installments.map((plan) => (
            <div key={plan.months} className="ml-6 mt-2 text-sm">
              <div className="flex justify-between">
                <span>{plan.months} months</span>
                <span className="font-medium">{formatCurrency(plan.monthlyAmount)}/mo</span>
              </div>
            </div>
          ))}
        </div>

        {card.benefits.special_offers.length > 0 && (
          <div className="p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center mb-2">
              <Tag className="w-4 h-4 mr-2 text-purple-500" />
              <p className="font-medium">Special Offers</p>
            </div>
            {card.benefits.special_offers.map((offer, index) => (
              <div key={index} className="ml-6 text-sm">
                <p className="font-medium">{offer.description}</p>
                <p className="text-gray-600">Valid: {offer.validity}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  function renderContent() {
    if (currentView === 'success') {
      return (
        <div className="h-[calc(100vh-10rem)] flex flex-col items-center justify-center px-4 bg-white">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-6">
            <Check className="w-8 h-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold mb-2">Payment Successful!</h2>
          <p className="text-gray-600 mb-2">
            Your payment of {formatCurrency(SAMPLE_DATA.transaction.amount)} has been processed.
          </p>
          <p className="text-gray-500 text-sm mb-8">
            Transaction ID: {Math.random().toString(36).substr(2, 9).toUpperCase()}
          </p>
          <Button 
            className="w-full" 
            size="lg"
            onClick={handleBackToMain}
          >
            Back to Home
          </Button>
        </div>
      );
    }

    if (currentView === 'details') {
      return (
        <div className="h-[calc(100vh-10rem)] overflow-y-auto bg-white">
          <div className="border-b sticky top-0 bg-white z-10">
            <div className="flex items-center p-4">
              <Button 
                variant="ghost" 
                size="sm" 
                className="mr-2"
                onClick={handleBackToMain}
              >
                <X className="w-4 h-4" />
              </Button>
              <h2 className="font-semibold">{activeCard?.type} Details</h2>
            </div>
          </div>
          <div className="p-4 pb-20">
            {activeCard && renderCardDetails(activeCard)}
          </div>
        </div>
      );
    }

    return (
      <div className="relative h-[calc(100vh-10rem)]">
        <div className="h-full overflow-y-auto">
          <Card className="rounded-none border-x-0">
            <CardContent className="pt-6">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold">{SAMPLE_DATA.transaction.merchant.name}</h3>
                  <p className="text-sm text-gray-600">{SAMPLE_DATA.transaction.merchant.category}</p>
                  <div className="mt-2 text-2xl font-bold">
                    {formatCurrency(SAMPLE_DATA.transaction.amount)}
                  </div>
                </div>
                {SAMPLE_DATA.transaction.merchant.special_offers?.length > 0 && (
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                    Offers
                  </span>
                )}
              </div>
            </CardContent>
          </Card>

          <div className="px-4 mt-6 pb-24">
            <h2 className="text-lg font-semibold mb-4">Select Payment Method</h2>
            <div className="space-y-3">
              {SAMPLE_DATA.cards.map((card) => (
                <Card 
                  key={card.id}
                  className={`cursor-pointer transition-all ${
                    selectedCard === card.id ? 'ring-2 ring-blue-500' : ''
                  }`}
                  onClick={() => handleCardClick(card)}
                >
                  <CardContent className="p-4">
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
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>

        <div className="absolute bottom-0 inset-x-0 p-4 bg-white border-t">
          <Button 
            className="w-full bg-blue-600 hover:bg-blue-700" 
            size="lg"
            onClick={handlePaymentClick}
          >
            Pay {formatCurrency(SAMPLE_DATA.transaction.amount)}
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
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
          <div className="relative h-[calc(100%-3rem)] bg-white">
            {renderContent()}
            
            {/* Home Indicator */}
            <div className="absolute bottom-1 left-1/2 -translate-x-1/2 w-[134px] h-[5px] bg-neutral-200 rounded-full" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default MobileDeviceDemo;