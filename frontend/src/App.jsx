import GraficoEnem from './components/GraficoEnem';

function App() {
  return (
    <div style={{ 
      width: '100vw', 
      minHeight: '100vh', 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center',
      backgroundColor: '#f0f2f5'
    }}>
      <GraficoEnem />
    </div>
  );
}

export default App;