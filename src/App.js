import React from 'react';
import ShinyText from './components/ShinyText';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <ShinyText 
          text="NASA API Explorer" 
          disabled={false} 
          speed={3} 
          className="title-text"
        />
        {/* Rest of your app content */}
      </header>
    </div>
  );
}

export default App; 