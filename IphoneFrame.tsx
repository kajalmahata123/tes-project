// components/IphoneFrame.tsx
import React from 'react';
import { Battery, Signal, Wifi } from 'lucide-react';

interface IphoneFrameProps {
  children: React.ReactNode;
}

const IphoneFrame: React.FC<IphoneFrameProps> = ({ children }) => {
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
          <div className="relative h-[calc(100%-3rem)]">
            <div className="h-full overflow-y-auto">
              {children}
            </div>

            {/* Home Indicator */}
            <div className="absolute bottom-1 left-1/2 -translate-x-1/2 w-[134px] h-[5px] bg-neutral-200 rounded-full" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default IphoneFrame;