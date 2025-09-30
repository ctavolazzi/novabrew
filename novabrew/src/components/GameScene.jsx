function GameScene({ scene, choices, onChoice, loading }) {
  return (
    <div className="game-scene">
      <div className="scene-content">
        <h2>{scene.title}</h2>
        <p>{scene.description}</p>
      </div>

      <div className="choices">
        {loading ? (
          <div className="loading">Generating choices...</div>
        ) : (
          <>
            {choices.map((choice, index) => (
              <button
                key={index}
                onClick={() => onChoice(choice)}
                className="choice-button"
              >
                {choice.text}
              </button>
            ))}
            <button
              onClick={() => onChoice({ text: "Do something else..." })}
              className="choice-button other"
            >
              Other...
            </button>
          </>
        )}
      </div>
    </div>
  )
}

export default GameScene