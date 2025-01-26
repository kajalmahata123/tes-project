import React, { useState, useEffect, useMemo } from 'react';
import { ArrowLeft, CreditCard, Info, CheckCircle2 } from 'lucide-react';

interface PaymentViewProps {
  amount: number;
  merchant: string;
  category: string;
  onBack: () => void;
}

interface CardRewards {
  baseRewards: {
    value: number;
    description: string;
  };
  specialOffer: {
    value: number;
    description: string;
  };
  totalValue: number;
  effectiveRate: number;
}

interface Card {
  id: number;
  name: string;
  network: string;
  last4: string;
  rewards: CardRewards;
}

interface AnalysisResponse {
  cards: Card[];
  transaction: {
    amount: number;
    merchant: string;
    category: string;
  };
  status: string;
}

const PaymentView: React.FC<PaymentViewProps> = ({ 
  amount,
  merchant,
  category,
  onBack 
}) => {
    const [selectedMethod, setSelectedMethod] = useState<number>(1);
    const [showSuccess, setShowSuccess] = useState(false);
    const [showCardInfo, setShowCardInfo] = useState<number | null>(null);
    const [cardRewards, setCardRewards] = useState<AnalysisResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const transactionId = useMemo(() => 'TXN' + Math.random().toString(36).substr(2, 9).toUpperCase(), []);

  useEffect(() => {
    const analyzeTransaction = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/analyze-purchase', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            amount,
            user_id: 'user123',
            merchant,
            category
          })
        });

        const data = await response.json();
        setCardRewards(data);
      } catch (error) {
        console.error('Failed to analyze transaction:', error);
      } finally {
        setLoading(false);
      }
    };

    analyzeTransaction();
  }, [amount, merchant, category]);

  const CardInfo: React.FC<{ card: Card }> = ({ card }) => (
    <div className="absolute right-0 top-0 mt-16 w-64 p-4 bg-white rounded-lg shadow-lg border border-gray-200 z-10">
      <h3 className="font-semibold mb-2">Rewards Breakdown</h3>
      <div className="text-sm mb-2">
        <div className="flex justify-between">
          <span className="text-gray-600">Base Rewards</span>
          <span className="font-medium">${card.rewards.baseRewards.value.toFixed(2)}</span>
        </div>
        <p className="text-xs text-gray-500">{card.rewards.baseRewards.description}</p>
      </div>
      <div className="text-sm mb-2">
        <div className="flex justify-between">
          <span className="text-gray-600">Special Offer</span>
          <span className="font-medium">${card.rewards.specialOffer.value.toFixed(2)}</span>
        </div>
        <p className="text-xs text-gray-500">{card.rewards.specialOffer.description}</p>
      </div>
      <div className="mt-3 pt-2 border-t">
        <div className="flex justify-between font-semibold">
          <span>Total Value</span>
          <span className="text-green-600">
            ${card.rewards.totalValue.toFixed(2)}
          </span>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          Effective reward rate: {card.rewards.effectiveRate.toFixed(1)}%
        </p>
      </div>
    </div>
  );

  if (loading || !cardRewards) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  if (showSuccess) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center px-4">
        <CheckCircle2 className="w-16 h-16 text-green-500 mb-6" />
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Payment Successful!
        </h1>
        <p className="text-gray-600 mb-6">
          Amount paid: ${amount.toFixed(2)}
        </p>
        <div className="bg-gray-50 rounded-lg p-4 w-full mb-8">
          <p className="text-sm text-gray-500">Transaction ID</p>
          <p className="text-gray-900 font-medium">{transactionId}</p>
        </div>
        <button
          onClick={onBack}
          className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold"
        >
          Done
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white px-4 py-4 flex items-center border-b border-gray-200">
        <button onClick={onBack} className="p-2 hover:bg-gray-100 rounded-full">
          <ArrowLeft className="w-6 h-6 text-gray-600" />
        </button>
        <h1 className="ml-3 text-xl font-semibold text-gray-900">Payment</h1>
      </div>

      <div className="px-4 py-8 bg-white mt-2">
        <p className="text-center text-gray-600 text-sm mb-2">Amount to Pay</p>
        <p className="text-center text-4xl font-bold text-gray-900">
          ${amount.toFixed(2)}
        </p>
      </div>

      <div className="px-4 py-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Select Payment Method
        </h2>
        <div className="space-y-3 mb-6">
          {cardRewards.cards.map(card => (
            <button
              key={card.id}
              onClick={() => setSelectedMethod(card.id)}
              className={`w-full p-4 rounded-xl border relative ${
                selectedMethod === card.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 bg-white'
              }`}
            >
              <div className="flex items-center">
                <div className={`w-5 h-5 rounded-full border-2 mr-4 ${
                  selectedMethod === card.id
                    ? 'border-blue-500 bg-blue-500'
                    : 'border-gray-300'
                }`}>
                  {selectedMethod === card.id && (
                    <div className="w-full h-full rounded-full bg-white scale-[0.4]" />
                  )}
                </div>
                
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                  <CreditCard className={`w-6 h-6 ${
                    selectedMethod === card.id ? 'text-blue-500' : 'text-gray-600'
                  }`} />
                </div>
                
                <div className="flex-1 ml-3 text-left">
                  <p className="font-medium text-gray-900">{card.name}</p>
                  <p className="text-sm text-gray-500">
                    {card.network} •••• {card.last4}
                    <span className="ml-2 text-green-600">
                      (${card.rewards.totalValue.toFixed(2)} value)
                    </span>
                  </p>
                </div>

                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowCardInfo(showCardInfo === card.id ? null : card.id);
                  }}
                  className="p-2 hover:bg-gray-100 rounded-full"
                >
                  <Info className="w-5 h-5 text-gray-400" />
                </button>
              </div>

              {showCardInfo === card.id && <CardInfo card={card} />}
            </button>
          ))}
        </div>
        
        <button 
          onClick={() => setShowSuccess(true)}
          className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
        >
          Pay ${amount.toFixed(2)}
        </button>
      </div>
    </div>
  );
};

export default PaymentView;