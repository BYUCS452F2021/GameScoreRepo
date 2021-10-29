import React, { useContext, useEffect, useState } from 'react'
import GameTile from '../Components/GameTile'
import AppContext from '../Contexts/AppContext'
import './Games.scss'

type GamePair = {
  value: string
  label: string
}

function Games() {
  const [allGames, setAllGames] = useState<GamePair[]>([])
  const appContext = useContext(AppContext)

  useEffect(() => {
    async function getAllGames() {
      const allGames = await appContext?.backend.getGames()
      setAllGames(allGames)
    }
    getAllGames()
  }, [appContext?.backend])

  return (
    <div className='games-page'>
      <h1>All Games</h1>
      <div className="Games">
        <div className="game-display">
          {allGames.map((game: GamePair) => React.createElement(GameTile, {gameId: game.value, gameName: game.label}))}
        </div>
      </div>
    </div>
  )
}

export default Games