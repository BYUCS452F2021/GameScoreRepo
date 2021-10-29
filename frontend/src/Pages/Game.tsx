import React, { useContext, useEffect, useState } from 'react'
import ScoreList from '../Components/ScoreList'
import AppContext from '../Contexts/AppContext'


type Props = {
  match: any
}

function Game(props: Props) {
  const appContext = useContext(AppContext)
  const [gameInfo, setGameInfo] = useState<any>(null)

  useEffect(() => {
    async function getGame() {
      const gameInfo = await appContext?.backend.getGame(props.match.params.id)
      setGameInfo(gameInfo)
    }
    getGame()
  }, [appContext?.backend, props.match.params.id])

  

  return (
    <div className="Game">
      {
        gameInfo &&
        <header className="Game-header">
          <h1>{gameInfo.name}</h1>
          <ScoreList gameId={props.match.params.id}/>
        </header>
      }
    </div>
  )
}

export default Game
