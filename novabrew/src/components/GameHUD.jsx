function GameHUD({ stats }) {
  return (
    <div className="game-hud">
      <div className="stat-bars">
        <div className="stat-bar">
          <div className="stat-label">HP</div>
          <div className="stat-background">
            <div
              className="stat-fill health"
              style={{ width: `${stats.health}%` }}
            >
              {stats.health}
            </div>
          </div>
        </div>

        <div className="stat-bar">
          <div className="stat-label">MP</div>
          <div className="stat-background">
            <div
              className="stat-fill mana"
              style={{ width: `${stats.mana}%` }}
            >
              {stats.mana}
            </div>
          </div>
        </div>
      </div>

      <div className="player-info">
        <div className="player-name">{stats.name}</div>
        <div className="player-level">Level {stats.level}</div>
      </div>
    </div>
  )
}

export default GameHUD