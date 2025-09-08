import React from 'react';
import { Home, FileText, Download } from 'lucide-react';

const Navigation = ({ currentView, onViewChange }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'causas', label: 'Causas', icon: FileText },
    { id: 'scraper', label: 'Scraper OJV', icon: Download },
  ];

  return (
    <nav className="flex overflow-x-auto">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = currentView === item.id;
        
        return (
          <button
            key={item.id}
            onClick={() => onViewChange(item.id)}
            className={`flex items-center gap-2 px-4 py-3 whitespace-nowrap border-b-2 transition-colors ${
              isActive
                ? 'border-blue-600 text-blue-600 bg-blue-50'
                : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50'
            }`}
          >
            <Icon className="h-4 w-4" />
            <span className="text-sm font-medium">{item.label}</span>
          </button>
        );
      })}
    </nav>
  );
};

export default Navigation;

