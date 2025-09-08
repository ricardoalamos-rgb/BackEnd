import React, { useState, useEffect } from 'react';
import { RefreshCw, Search, Plus, ArrowLeft, Menu, X, Wifi, WifiOff } from 'lucide-react';
import './App.css';

// Importar componentes
import CausaCard from './components/CausaCard';
import SearchBar from './components/SearchBar';
import CausaDetail from './components/CausaDetail';
import GestionForm from './components/GestionForm';
import Navigation from './components/Navigation';
import ScraperPanel from './components/ScraperPanel';

// Importar hooks y utilidades
import { useCausas } from './hooks/useCausas';
import { apiClient } from './lib/api';
import { initWebSocket, getConnectionStatus } from './lib/websocket';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedCausa, setSelectedCausa] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [lastSync, setLastSync] = useState(null);

  const { causas, loading, error, refreshCausas } = useCausas();

  useEffect(() => {
    // Inicializar WebSocket
    initWebSocket();
    
    // Monitorear estado de conexión
    const interval = setInterval(() => {
      setConnectionStatus(getConnectionStatus());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const filteredCausas = causas.filter(causa =>
    causa.caratulado.toLowerCase().includes(searchTerm.toLowerCase()) ||
    causa.rol.toLowerCase().includes(searchTerm.toLowerCase()) ||
    causa.tribunal.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleViewCausa = (causa) => {
    setSelectedCausa(causa);
    setCurrentView('detail');
  };

  const handleBackFromDetail = () => {
    setSelectedCausa(null);
    setCurrentView('causas');
  };

  const handleAddGestion = (causa) => {
    setSelectedCausa(causa);
    setCurrentView('add-gestion');
  };

  const handleSync = async () => {
    try {
      await refreshCausas();
      setLastSync(new Date());
    } catch (error) {
      console.error('Error sincronizando:', error);
    }
  };

  const renderHeader = () => (
    <header className="bg-blue-600 text-white p-4 sticky top-0 z-50">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {currentView !== 'dashboard' && (
            <button
              onClick={() => setCurrentView('dashboard')}
              className="p-1 hover:bg-blue-700 rounded"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
          )}
          <h1 className="text-xl font-bold">CRM Legal</h1>
        </div>

        <div className="flex items-center gap-2">
          {/* Indicador de conexión */}
          <div className="flex items-center gap-1">
            {connectionStatus === 'connected' ? (
              <Wifi className="h-4 w-4 text-green-400" />
            ) : (
              <WifiOff className="h-4 w-4 text-red-400" />
            )}
            <span className="text-xs">
              {connectionStatus === 'connected' ? 'En línea' : 'Sin conexión'}
            </span>
          </div>

          {/* Botón de sincronización */}
          <button
            onClick={handleSync}
            disabled={loading}
            className="p-2 hover:bg-blue-700 rounded-full"
            title="Sincronizar"
          >
            <RefreshCw className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
          </button>

          {/* Menú móvil */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 hover:bg-blue-700 rounded"
          >
            {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Información de última sincronización */}
      {lastSync && (
        <div className="text-xs text-blue-200 mt-2">
          Última sincronización: {lastSync.toLocaleTimeString()}
        </div>
      )}
    </header>
  );

  const renderDashboard = () => (
    <div className="p-4 space-y-6">
      {/* Estadísticas */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg p-4 shadow">
          <div className="text-2xl font-bold text-blue-600">{causas.length}</div>
          <div className="text-sm text-gray-600">Total Causas</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow">
          <div className="text-2xl font-bold text-green-600">
            {causas.filter(c => c.estado === 'Activa').length}
          </div>
          <div className="text-sm text-gray-600">Activas</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow">
          <div className="text-2xl font-bold text-orange-600">
            {causas.filter(c => c.estado === 'En Tramitación').length}
          </div>
          <div className="text-sm text-gray-600">En Tramitación</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow">
          <div className="text-2xl font-bold text-red-600">
            {causas.filter(c => c.estado === 'Terminada').length}
          </div>
          <div className="text-sm text-gray-600">Terminadas</div>
        </div>
      </div>

      {/* Acciones rápidas */}
      <div className="bg-white rounded-lg p-4 shadow">
        <h2 className="text-lg font-semibold mb-4">Acciones Rápidas</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={() => setCurrentView('causas')}
            className="flex items-center gap-3 p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
          >
            <Search className="h-6 w-6 text-blue-600" />
            <div className="text-left">
              <div className="font-medium">Ver Causas</div>
              <div className="text-sm text-gray-600">Buscar y gestionar causas</div>
            </div>
          </button>

          <button
            onClick={() => setCurrentView('scraper')}
            className="flex items-center gap-3 p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
          >
            <RefreshCw className="h-6 w-6 text-green-600" />
            <div className="text-left">
              <div className="font-medium">Scraper OJV</div>
              <div className="text-sm text-gray-600">Actualizar desde OJV</div>
            </div>
          </button>

          <button
            onClick={handleSync}
            className="flex items-center gap-3 p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors"
          >
            <RefreshCw className="h-6 w-6 text-purple-600" />
            <div className="text-left">
              <div className="font-medium">Sincronizar</div>
              <div className="text-sm text-gray-600">Actualizar datos</div>
            </div>
          </button>
        </div>
      </div>

      {/* Causas recientes */}
      <div className="bg-white rounded-lg p-4 shadow">
        <h2 className="text-lg font-semibold mb-4">Causas Recientes</h2>
        <div className="space-y-3">
          {causas.slice(0, 5).map((causa) => (
            <div
              key={causa.id}
              onClick={() => handleViewCausa(causa)}
              className="flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 rounded-lg cursor-pointer transition-colors"
            >
              <div>
                <div className="font-medium">{causa.rol}</div>
                <div className="text-sm text-gray-600 truncate">{causa.caratulado}</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium">{causa.estado}</div>
                <div className="text-xs text-gray-500">{causa.tribunal}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderCausas = () => (
    <div className="p-4">
      <SearchBar
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        placeholder="Buscar por caratulado, rol o tribunal..."
      />

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          Error: {error}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center items-center py-8">
          <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
          <span className="ml-2">Cargando causas...</span>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredCausas.map((causa) => (
            <CausaCard
              key={causa.id}
              causa={causa}
              onView={() => handleViewCausa(causa)}
              onAddGestion={() => handleAddGestion(causa)}
            />
          ))}

          {filteredCausas.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              {searchTerm ? 'No se encontraron causas que coincidan con la búsqueda' : 'No hay causas disponibles'}
            </div>
          )}
        </div>
      )}
    </div>
  );

  const renderContent = () => {
    switch (currentView) {
      case 'dashboard':
        return renderDashboard();
      case 'causas':
        return renderCausas();
      case 'detail':
        return (
          <CausaDetail
            causa={selectedCausa}
            onBack={handleBackFromDetail}
            onAddGestion={() => setCurrentView('add-gestion')}
          />
        );
      case 'add-gestion':
        return (
          <GestionForm
            causa={selectedCausa}
            onBack={() => setCurrentView('detail')}
            onSave={() => {
              setCurrentView('detail');
              refreshCausas();
            }}
          />
        );
      case 'scraper':
        return <ScraperPanel apiClient={apiClient} />;
      default:
        return renderDashboard();
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {renderHeader()}

      {/* Navegación móvil */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-b">
          <Navigation
            currentView={currentView}
            onViewChange={(view) => {
              setCurrentView(view);
              setIsMenuOpen(false);
            }}
          />
        </div>
      )}

      {/* Navegación desktop */}
      <div className="hidden md:block bg-white border-b">
        <Navigation
          currentView={currentView}
          onViewChange={setCurrentView}
        />
      </div>

      {/* Contenido principal */}
      <main className="pb-4">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;

