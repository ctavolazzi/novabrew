import { useState, useEffect } from 'react'
import GameHUD from './components/GameHUD'
import GameScene from './components/GameScene'
import { generateScene } from './services/gameService'
import TestPanel from './components/TestPanel'
import './App.css'

function App() {
  const [playerStats, setPlayerStats] = useState({
    health: 100,
    mana: 100,
    name: 'Sam Iker',
    level: 1
  });

  const [currentScene, setCurrentScene] = useState({
    description: "Sam Iker wakes up from a vivid dream about flying around a skyscraper. The morning sun filters through the window, and the remnants of the dream still linger...",
    title: "Awakening"
  });

  const [choices, setChoices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('🎮 Game Initializing');
    console.log('Initial Player Stats:', playerStats);
    console.log('Initial Scene:', currentScene);
    fetchNewChoices();
  }, []);

  const fetchNewChoices = async () => {
    console.group('🎲 Fetching New Choices');
    console.log('Current Scene:', currentScene);
    setLoading(true);
    setError(null);

    try {
      console.time('generateScene');
      const response = await generateScene(currentScene);
      console.timeEnd('generateScene');

      console.log('🎯 New Choices Generated:', response.choices);
      setChoices(response.choices);
    } catch (error) {
      console.error('❌ Error generating choices:', error);
      setError('Failed to connect to Ollama. Make sure Ollama is running on your system.');
    } finally {
      setLoading(false);
      console.groupEnd();
    }
  };

  const handleChoice = async (choice) => {
    console.group('🎯 Player Choice');
    console.log('Selected Choice:', choice);
    console.log('Previous Stats:', playerStats);

    setLoading(true);
    try {
      // Update player stats
      setPlayerStats(prev => {
        const newStats = {
          ...prev,
          health: Math.max(0, Math.min(100, prev.health + (choice.healthEffect || 0))),
          mana: Math.max(0, Math.min(100, prev.mana + (choice.manaEffect || 0)))
        };
        console.log('Updated Stats:', newStats);
        return newStats;
      });

      // Generate new scene
      console.time('generateScene');
      const newScene = await generateScene(currentScene, choice);
      console.timeEnd('generateScene');

      console.log('New Scene:', newScene);
      setCurrentScene(newScene.scene);
      setChoices(newScene.choices);
    } catch (error) {
      console.error('❌ Error processing choice:', error);
      setError('Failed to process choice. Please try again.');
    } finally {
      setLoading(false);
      console.groupEnd();
    }
  };

  // Add error boundary
  if (error) {
    console.error('🚨 Game Error State:', error);
  }

  return (
    <div className="game-container">
      <h1>Teleport Massive CYOA</h1>
      {error && (
        <div className="error-message">
          <p>🚨 {error}</p>
          <button onClick={() => {
            console.log('🔄 Retrying after error...');
            fetchNewChoices();
          }}>
            Try Again
          </button>
        </div>
      )}
      <GameHUD stats={playerStats} />
      <GameScene
        scene={currentScene}
        choices={choices}
        onChoice={handleChoice}
        loading={loading}
      />

      {/* Add debug panel in development */}
      {import.meta.env.DEV && (
        <div className="debug-panel">
          <h3>🔍 Debug Info</h3>
          <pre>
            {JSON.stringify({
              playerStats,
              currentScene,
              choices,
              loading,
              error
            }, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}

export default App
