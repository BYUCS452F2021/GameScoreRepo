import React from 'react'
import { useHistory } from 'react-router-dom'
import './GameTile.scss'

type Props = {
    gameId: string
    gameName: string
    imageUrl: string
}

function GameTile(props: Props) {
  const history = useHistory()

  function onClick() {
    history.push('/game/' + props.gameName)
  }

  return (
    <div className="game-tile" onClick={onClick} key={props.gameId}>
        <img className="game-picture" src={props.imageUrl} alt={props.gameName}/>
        <div className="game-title">
            {props.gameName}
        </div>
    </div>
  )
}

export default GameTile