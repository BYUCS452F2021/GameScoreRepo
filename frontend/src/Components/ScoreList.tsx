import React, { useContext, useEffect, useState } from 'react'
import AppContext from '../Contexts/AppContext'
import './ScoreList.scss'


type Param =  {
  description: string;
  name: string;
  value: string;
}

type Score =  {
  game: string;
  username: string;
  timestamp: string;
  params: Array<Param>;
}

type Props = {
  gameName?: string
  userId?: string
}


function ScoreList(props: Props) {
  const [scores, setScores] = useState<Score[]>([])
  const appContext = useContext(AppContext)

  useEffect(() => {
    async function getScores() {
      const scores = props.gameName ? await appContext?.backend.getScores(props.gameName) : await appContext?.backend.getUserScores(props.userId)
      setScores(scores)
    }
    getScores()
  }, [appContext?.backend, props.gameName, props.userId])

  function ScoreItem(score: Score) {
    return (
      <div className='list-item' key={score.username + score.timestamp + score.game}>
        {
          score.params.map((element: Param) => {
            return (
              <div className="info-item">
                {element.name + ': ' + element.value}
              </div>
            )
          })
        }
        <div className="info-item">
          {'Username: ' + score.username}
        </div>
      </div>
    )
  }

  return (
    <div className="score-page">
      <div className="list-container">
        {scores.map((score: Score) => ScoreItem(score))}
      </div>
    </div>
  )
}

export default ScoreList
