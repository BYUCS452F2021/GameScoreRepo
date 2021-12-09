import React, { useContext, useEffect, useState } from 'react'
import GameTile from '../Components/GameTile'
import AppContext from '../Contexts/AppContext'
import './Games.scss'

type Param = {
  description: string;
  name: string;
}

type Game = {
  value: any;
  label: any;
  description: any;
  availableParams: Array<Param>;
  imageLink: any;
  owner: any;
  publisher: any;
}

function Games() {
  const [allGames, setAllGames] = useState<Game[]>([])
  const appContext = useContext(AppContext)

  useEffect(() => {
    async function getAllGames() {
      const allGames = await appContext?.backend.getGames()
      console.log(allGames)
      setAllGames(allGames)
    }
    getAllGames()
  }, [appContext?.backend])

  return (
    <div className='games-page'>
      <h1>All Games</h1>
      <div className="Games">
        <div className="game-display">
          {allGames.map((game: Game) => React.createElement(GameTile, {gameId: game.value, gameName: game.label, imageUrl: game.imageLink}))}
        </div>
      </div>
    </div>
  )
}

export default Games