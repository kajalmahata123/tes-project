import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { 
  CreditCard,
  Gift,
  Shield,
  Clock,
  DollarSign,
  Calendar,
  TrendingUp,
  Tag,
  Percent,
  Star,
  Check
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
          },
          purchase_protection: {
            duration: "90 days",
            coverage: "Up to $1,000 per claim"
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
          },
          purchase_protection: {
            duration: "120 days",
            coverage: "Up to $2,000 per claim"
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

const CheckoutCardSelection = () => {
  const [selectedCard, setSelectedCard] = useState(SAMPLE_DATA.cards.find(card => card.isDefault)?.id);
  const [activeTab, setActiveTab] = useState('cards');

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  return (
    <div className="max-w-3xl mx-auto p-4 bg-gray-50 min-h-screen">
      {/* Transaction Summary */}
      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-semibold">{SAMPLE_DATA.transaction.merchant.name}</h3>
              <p className="text-sm text-gray-600">
                {SAMPLE_DATA.transaction.merchant.category} • {SAMPLE_DATA.transaction.merchant.merchant_type}
              </p>
              <div className="mt-2 text-2xl font-bold">
                {formatCurrency(SAMPLE_DATA.transaction.amount)}
              </div>
            </div>
            {SAMPLE_DATA.transaction.merchant.special_offers?.length > 0 && (
              <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                Special Offers Available
              </span>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Main Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid grid-cols-3 gap-4 mb-6">
          <TabsTrigger value="cards" className="flex items-center">
            <CreditCard className="w-4 h-4 mr-2" />
            Cards
          </TabsTrigger>
          <TabsTrigger value="installments" className="flex items-center">
            <Calendar className="w-4 h-4 mr-2" />
            Installments
          </TabsTrigger>
          <TabsTrigger value="benefits" className="flex items-center">
            <Gift className="w-4 h-4 mr-2" />
            Benefits
          </TabsTrigger>
        </TabsList>

        {/* Cards Tab */}
        <TabsContent value="cards">
          <div className="space-y-4">
            {SAMPLE_DATA.cards.map((card) => (
              <Card 
                key={card.id}
                className={`cursor-pointer transition-all ${
                  selectedCard === card.id ? 'ring-2 ring-blue-500' : 'hover:bg-gray-50'
                }`}
                onClick={() => setSelectedCard(card.id)}
              >
                <CardContent className="p-4">
                  {/* Card Header */}
                  <div className="flex items-start justify-between">
                    <div className="flex items-center">
                      <CreditCard className={`w-5 h-5 ${
                        selectedCard === card.id ? 'text-blue-500' : 'text-gray-400'
                      }`} />
                      <div className="ml-3">
                        <p className="font-medium">{card.type}</p>
                        <p className="text-sm text-gray-600">
                          {card.network} •••• {card.last4}
                          {card.isDefault && 
                            <span className="ml-2 text-blue-600">(Default)</span>
                          }
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      {card.benefits.cashback && (
                        <p className="text-green-600 font-medium">
                          {card.benefits.cashback * 100}% cashback
                        </p>
                      )}
                      {card.benefits.points && (
                        <p className="text-blue-600 font-medium">
                          {card.benefits.points}x points
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Expanded Card Details */}
                  {selectedCard === card.id && (
                    <div className="mt-4 space-y-4">
                      {/* Quick Benefits */}
                      <div className="grid grid-cols-2 gap-4">
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

                      {/* Special Offers */}
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
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Installments Tab */}
        <TabsContent value="installments">
          <div className="space-y-4">
            {SAMPLE_DATA.cards.map((card) => (
              <Card key={card.id}>
                <CardHeader>
                  <CardTitle className="text-lg flex items-center">
                    <CreditCard className="w-5 h-5 mr-2" />
                    {card.type}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {card.benefits.installments.map((plan) => (
                      <div key={plan.months} className="p-4 bg-gray-50 rounded-lg">
                        <div className="flex justify-between items-center mb-2">
                          <span className="font-medium">{plan.months} Monthly Payments</span>
                          <span className="text-lg font-bold text-blue-600">
                            {formatCurrency(plan.monthlyAmount)}/mo
                          </span>
                        </div>
                        <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                          <div>Interest: {(plan.interest * 100).toFixed(2)}%</div>
                          <div>Fee: {formatCurrency(plan.processingFee)}</div>
                          <div>Total: {formatCurrency(plan.totalAmount)}</div>
                          <div>Min Purchase: {formatCurrency(plan.minAmount)}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Benefits Tab */}
        <TabsContent value="benefits">
          <div className="space-y-4">
            {SAMPLE_DATA.cards.map((card) => (
              <Card key={card.id}>
                <CardHeader>
                  <CardTitle className="text-lg flex items-center">
                    <Star className="w-5 h-5 mr-2" />
                    {card.type} Benefits
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Protection Benefits */}
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <h4 className="font-medium mb-3 flex items-center">
                        <Shield className="w-4 h-4 mr-2 text-blue-500" />
                        Protection Benefits
                      </h4>
                      <div className="space-y-3 ml-6">
                        {Object.entries(card.benefits.protection).map(([key, value]) => (
                          <div key={key} className="text-sm">
                            <p className="font-medium capitalize">{key.replace('_', ' ')}</p>
                            <p className="text-gray-600">Duration: {value.duration}</p>
                            <p className="text-gray-600">Coverage: {value.coverage}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Special Offers */}
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <h4 className="font-medium mb-3 flex items-center">
                        <Gift className="w-4 h-4 mr-2 text-purple-500" />
                        Special Offers
                      </h4>
                      <div className="space-y-3 ml-6">
                        {card.benefits.special_offers.map((offer, index) => (
                          <div key={index} className="text-sm">
                            <p className="font-medium">{offer.description}</p>
                            <p className="text-gray-600">Valid: {offer.validity}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default CheckoutCardSelection;