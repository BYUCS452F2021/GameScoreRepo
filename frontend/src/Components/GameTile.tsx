import React from 'react'
import { useHistory } from 'react-router-dom'
import './GameTile.scss'

type Props = {
    gameId: string
    gameName: string
}

function GameTile(props: Props) {
  const history = useHistory()
  const imageUrl = process.env.PUBLIC_URL + '/GameImages/' + props.gameId + '.jpeg'

  function onClick() {
    history.push('/game/' + props.gameId)
  }

  return (
    <div className="game-tile" onClick={onClick} key={props.gameId}>
        <img className="game-picture" src={imageUrl} alt={props.gameName}/>
        <div className="game-title">
            {props.gameName}
        </div>
    </div>
  )
}

export default GameTile