import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { AlertCircle, Download, RefreshCw, Search, Settings, CheckCircle, XCircle } from 'lucide-react';

const ScraperPanel = ({ apiClient }) => {
  const [scraperState, setScraperState] = useState({
    isLoggedIn: false,
    isLoading: false,
    lastUpdate: null,
    totalCausas: 0,
    causasPorCompetencia: {}
  });

  const [loginForm, setLoginForm] = useState({
    username: '',
    password: '',
    authType: 'clave_unica'
  });

  const [searchForm, setSearchForm] = useState({
    rol: '',
    competencia: 'civil'
  });

  const [massiveScrapingForm, setMassiveScrapingForm] = useState({
    roles: '',
    competencias: ['civil', 'laboral', 'penal', 'cobranza', 'familia'],
    updateDb: true
  });

  const [results, setResults] = useState([]);
  const [logs, setLogs] = useState([]);

  const competencias = [
    { value: 'civil', label: 'Civil' },
    { value: 'laboral', label: 'Laboral' },
    { value: 'penal', label: 'Penal' },
    { value: 'cobranza', label: 'Cobranza' },
    { value: 'familia', label: 'Familia' },
    { value: 'suprema', label: 'Suprema' },
    { value: 'apelaciones', label: 'Apelaciones' },
    { value: 'disciplinario', label: 'Disciplinario' }
  ];

  useEffect(() => {
    loadScraperStatus();
  }, []);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { timestamp, message, type }]);
  };

  const loadScraperStatus = async () => {
    try {
      const response = await apiClient.get('/scraper/estado-scraper');
      if (response.data.success) {
        setScraperState(prev => ({
          ...prev,
          totalCausas: response.data.estado.total_causas,
          causasPorCompetencia: response.data.estado.causas_por_competencia,
          lastUpdate: response.data.estado.ultima_actualizacion
        }));
      }
    } catch (error) {
      addLog('Error cargando estado del scraper', 'error');
    }
  };

  const handleLogin = async () => {
    if (!loginForm.username || !loginForm.password) {
      addLog('Usuario y contraseña son requeridos', 'error');
      return;
    }

    setScraperState(prev => ({ ...prev, isLoading: true }));
    addLog('Iniciando sesión en OJV...', 'info');

    try {
      const response = await apiClient.post('/scraper/login', loginForm);
      
      if (response.data.success) {
        setScraperState(prev => ({ 
          ...prev, 
          isLoggedIn: true, 
          isLoading: false 
        }));
        addLog('Sesión iniciada exitosamente', 'success');
      } else {
        throw new Error(response.data.error || 'Error en login');
      }
    } catch (error) {
      setScraperState(prev => ({ ...prev, isLoading: false }));
      addLog(`Error en login: ${error.message}`, 'error');
    }
  };

  const handleSearchCausa = async () => {
    if (!searchForm.rol) {
      addLog('El rol es requerido', 'error');
      return;
    }

    setScraperState(prev => ({ ...prev, isLoading: true }));
    addLog(`Buscando causa con rol: ${searchForm.rol}`, 'info');

    try {
      const response = await apiClient.post('/scraper/buscar-causa', searchForm);
      
      if (response.data.success) {
        setResults(response.data.causas);
        addLog(`Se encontraron ${response.data.total} causas`, 'success');
      } else {
        throw new Error(response.data.error || 'Error en búsqueda');
      }
    } catch (error) {
      addLog(`Error en búsqueda: ${error.message}`, 'error');
    } finally {
      setScraperState(prev => ({ ...prev, isLoading: false }));
    }
  };

  const handleMassiveScraping = async () => {
    const rolesList = massiveScrapingForm.roles
      .split('\n')
      .map(rol => rol.trim())
      .filter(rol => rol.length > 0);

    if (rolesList.length === 0) {
      addLog('Se requiere al menos un rol', 'error');
      return;
    }

    setScraperState(prev => ({ ...prev, isLoading: true }));
    addLog(`Iniciando scraping masivo de ${rolesList.length} roles`, 'info');

    try {
      const response = await apiClient.post('/scraper/scraping-masivo', {
        roles: rolesList,
        competencias: massiveScrapingForm.competencias,
        actualizar_bd: massiveScrapingForm.updateDb
      });
      
      if (response.data.success) {
        setResults(response.data.causas);
        addLog(`Scraping completado: ${response.data.total_causas_scrapeadas} causas procesadas`, 'success');
        addLog(`${response.data.causas_nuevas} causas nuevas, ${response.data.causas_actualizadas} actualizadas`, 'info');
        
        // Recargar estado
        loadScraperStatus();
      } else {
        throw new Error(response.data.error || 'Error en scraping masivo');
      }
    } catch (error) {
      addLog(`Error en scraping masivo: ${error.message}`, 'error');
    } finally {
      setScraperState(prev => ({ ...prev, isLoading: false }));
    }
  };

  const handleSyncWithSheets = async () => {
    setScraperState(prev => ({ ...prev, isLoading: true }));
    addLog('Sincronizando con Google Sheets...', 'info');

    try {
      const response = await apiClient.post('/scraper/sincronizar-con-sheets');
      
      if (response.data.success) {
        addLog(`Sincronización completada: ${response.data.causas_sincronizadas} causas`, 'success');
      } else {
        throw new Error(response.data.error || 'Error en sincronización');
      }
    } catch (error) {
      addLog(`Error en sincronización: ${error.message}`, 'error');
    } finally {
      setScraperState(prev => ({ ...prev, isLoading: false }));
    }
  };

  const clearLogs = () => {
    setLogs([]);
  };

  return (
    <div className="space-y-6">
      {/* Estado del Scraper */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Estado del Scraper OJV
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{scraperState.totalCausas}</div>
              <div className="text-sm text-gray-600">Total Causas</div>
            </div>
            <div className="text-center">
              <Badge variant={scraperState.isLoggedIn ? "success" : "secondary"}>
                {scraperState.isLoggedIn ? "Conectado" : "Desconectado"}
              </Badge>
              <div className="text-sm text-gray-600 mt-1">Estado OJV</div>
            </div>
            <div className="text-center">
              <div className="text-sm font-medium">
                {scraperState.lastUpdate ? 
                  new Date(scraperState.lastUpdate).toLocaleDateString() : 
                  'Nunca'
                }
              </div>
              <div className="text-sm text-gray-600">Última Actualización</div>
            </div>
            <div className="text-center">
              <Button 
                onClick={loadScraperStatus} 
                variant="outline" 
                size="sm"
                disabled={scraperState.isLoading}
              >
                <RefreshCw className={`h-4 w-4 ${scraperState.isLoading ? 'animate-spin' : ''}`} />
              </Button>
              <div className="text-sm text-gray-600 mt-1">Actualizar</div>
            </div>
          </div>

          {/* Causas por Competencia */}
          {Object.keys(scraperState.causasPorCompetencia).length > 0 && (
            <div className="mt-4">
              <h4 className="text-sm font-medium mb-2">Causas por Competencia:</h4>
              <div className="flex flex-wrap gap-2">
                {Object.entries(scraperState.causasPorCompetencia).map(([comp, count]) => (
                  <Badge key={comp} variant="outline">
                    {comp}: {count}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Tabs principales */}
      <Tabs defaultValue="login" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="login">Login</TabsTrigger>
          <TabsTrigger value="search">Búsqueda</TabsTrigger>
          <TabsTrigger value="massive">Masivo</TabsTrigger>
          <TabsTrigger value="logs">Logs</TabsTrigger>
        </TabsList>

        {/* Tab de Login */}
        <TabsContent value="login">
          <Card>
            <CardHeader>
              <CardTitle>Iniciar Sesión en OJV</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="authType">Tipo de Autenticación</Label>
                <select
                  id="authType"
                  className="w-full p-2 border rounded-md"
                  value={loginForm.authType}
                  onChange={(e) => setLoginForm(prev => ({ ...prev, authType: e.target.value }))}
                >
                  <option value="clave_unica">Clave Única</option>
                  <option value="clave_poder_judicial">Clave Poder Judicial</option>
                </select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="username">Usuario</Label>
                <Input
                  id="username"
                  type="text"
                  value={loginForm.username}
                  onChange={(e) => setLoginForm(prev => ({ ...prev, username: e.target.value }))}
                  placeholder="Ingrese su usuario"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Contraseña</Label>
                <Input
                  id="password"
                  type="password"
                  value={loginForm.password}
                  onChange={(e) => setLoginForm(prev => ({ ...prev, password: e.target.value }))}
                  placeholder="Ingrese su contraseña"
                />
              </div>

              <Button 
                onClick={handleLogin} 
                disabled={scraperState.isLoading || scraperState.isLoggedIn}
                className="w-full"
              >
                {scraperState.isLoading ? (
                  <>
                    <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                    Iniciando Sesión...
                  </>
                ) : scraperState.isLoggedIn ? (
                  <>
                    <CheckCircle className="mr-2 h-4 w-4" />
                    Sesión Activa
                  </>
                ) : (
                  'Iniciar Sesión'
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tab de Búsqueda Individual */}
        <TabsContent value="search">
          <Card>
            <CardHeader>
              <CardTitle>Búsqueda Individual</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="searchRol">Número de Rol</Label>
                  <Input
                    id="searchRol"
                    type="text"
                    value={searchForm.rol}
                    onChange={(e) => setSearchForm(prev => ({ ...prev, rol: e.target.value }))}
                    placeholder="Ej: 12345-2023"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="searchCompetencia">Competencia</Label>
                  <select
                    id="searchCompetencia"
                    className="w-full p-2 border rounded-md"
                    value={searchForm.competencia}
                    onChange={(e) => setSearchForm(prev => ({ ...prev, competencia: e.target.value }))}
                  >
                    {competencias.map(comp => (
                      <option key={comp.value} value={comp.value}>{comp.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              <Button 
                onClick={handleSearchCausa} 
                disabled={scraperState.isLoading || !scraperState.isLoggedIn}
                className="w-full"
              >
                {scraperState.isLoading ? (
                  <>
                    <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                    Buscando...
                  </>
                ) : (
                  <>
                    <Search className="mr-2 h-4 w-4" />
                    Buscar Causa
                  </>
                )}
              </Button>

              {!scraperState.isLoggedIn && (
                <div className="flex items-center gap-2 text-amber-600 text-sm">
                  <AlertCircle className="h-4 w-4" />
                  Debe iniciar sesión primero
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tab de Scraping Masivo */}
        <TabsContent value="massive">
          <Card>
            <CardHeader>
              <CardTitle>Scraping Masivo</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="massiveRoles">Roles (uno por línea)</Label>
                <Textarea
                  id="massiveRoles"
                  value={massiveScrapingForm.roles}
                  onChange={(e) => setMassiveScrapingForm(prev => ({ ...prev, roles: e.target.value }))}
                  placeholder="12345-2023&#10;67890-2023&#10;11111-2024"
                  rows={6}
                />
              </div>

              <div className="space-y-2">
                <Label>Competencias a Buscar</Label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                  {competencias.map(comp => (
                    <label key={comp.value} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={massiveScrapingForm.competencias.includes(comp.value)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setMassiveScrapingForm(prev => ({
                              ...prev,
                              competencias: [...prev.competencias, comp.value]
                            }));
                          } else {
                            setMassiveScrapingForm(prev => ({
                              ...prev,
                              competencias: prev.competencias.filter(c => c !== comp.value)
                            }));
                          }
                        }}
                      />
                      <span className="text-sm">{comp.label}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="updateDb"
                  checked={massiveScrapingForm.updateDb}
                  onChange={(e) => setMassiveScrapingForm(prev => ({ ...prev, updateDb: e.target.checked }))}
                />
                <Label htmlFor="updateDb">Actualizar base de datos</Label>
              </div>

              <div className="flex gap-2">
                <Button 
                  onClick={handleMassiveScraping} 
                  disabled={scraperState.isLoading || !scraperState.isLoggedIn}
                  className="flex-1"
                >
                  {scraperState.isLoading ? (
                    <>
                      <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                      Procesando...
                    </>
                  ) : (
                    <>
                      <Download className="mr-2 h-4 w-4" />
                      Iniciar Scraping
                    </>
                  )}
                </Button>

                <Button 
                  onClick={handleSyncWithSheets} 
                  disabled={scraperState.isLoading}
                  variant="outline"
                >
                  Sincronizar Sheets
                </Button>
              </div>

              {!scraperState.isLoggedIn && (
                <div className="flex items-center gap-2 text-amber-600 text-sm">
                  <AlertCircle className="h-4 w-4" />
                  Debe iniciar sesión primero
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tab de Logs */}
        <TabsContent value="logs">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Logs del Scraper</CardTitle>
              <Button onClick={clearLogs} variant="outline" size="sm">
                Limpiar
              </Button>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-50 rounded-md p-4 max-h-96 overflow-y-auto">
                {logs.length === 0 ? (
                  <div className="text-gray-500 text-center">No hay logs disponibles</div>
                ) : (
                  <div className="space-y-2">
                    {logs.map((log, index) => (
                      <div key={index} className="flex items-start gap-2 text-sm">
                        <span className="text-gray-400 font-mono">{log.timestamp}</span>
                        {log.type === 'error' && <XCircle className="h-4 w-4 text-red-500 mt-0.5" />}
                        {log.type === 'success' && <CheckCircle className="h-4 w-4 text-green-500 mt-0.5" />}
                        {log.type === 'info' && <AlertCircle className="h-4 w-4 text-blue-500 mt-0.5" />}
                        <span className={`${
                          log.type === 'error' ? 'text-red-700' : 
                          log.type === 'success' ? 'text-green-700' : 
                          'text-gray-700'
                        }`}>
                          {log.message}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Resultados */}
      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Resultados ({results.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {results.map((causa, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                    <div><strong>Rol/RIT:</strong> {causa.rit || causa.rol}</div>
                    <div><strong>Competencia:</strong> {causa.competencia}</div>
                    <div><strong>Caratulado:</strong> {causa.caratulado}</div>
                    <div><strong>Tribunal:</strong> {causa.tribunal}</div>
                    <div><strong>Fecha Ingreso:</strong> {causa.fecha_ingreso}</div>
                    <div><strong>Estado:</strong> {causa.estado_causa || causa.estado}</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ScraperPanel;

