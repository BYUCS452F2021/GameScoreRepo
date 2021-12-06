import React, { useEffect, useState } from 'react'
import ReactDOM from 'react-dom'
import AppContext from '../Contexts/AppContext'
import Button from './Button'
import Select from 'react-select'
import './ScoreModal.scss'
import FluidInput from './FluidInput'

type Props = {
  onClose: Function
}

type GameDetails = {
  value: string
  label: string
}

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

function ScoreModal(props: Props) {
  const appContext = React.useContext(AppContext)
  const [options, setOptions] = useState<GameDetails[]>([])
  const [currGame, setCurrGame] = useState<Game|null>(null)
  const [currScore, setCurrScore] = useState<Array<number | null>>([null])
  const [scoreError, setScoreError] = useState<boolean>(false)

  useEffect(() => {
    async function getOptions() {
      const options = await appContext?.backend.getGames()
      setOptions(options)
    }
    getOptions()
  }, [appContext?.backend])

  async function onSubmit() {
    if (currGame) {
      const submittedScores = currGame.availableParams.map(function(e, i) {
        return [e.name, currScore[i]];
      });
      console.log(submittedScores)

      const result = await appContext?.backend.submitScore(currGame.label, submittedScores, appContext.currUser)
      if (result.success) {
        setScoreError(false)
        props.onClose()
      }
    }
    setScoreError(true)
  }
  
  function updateScore(e: number | null, idx: number) {
    const currScores = [...currScore.slice(0, idx), e, ...currScore.slice(idx+1)]
    setCurrScore(currScores)
  }

  function assertIsGame(data: unknown): data is Game {
    if (!data) {
      return false
    }
    return true
  }

  function updateGame(e: unknown) {
    if (assertIsGame(e)) {
      setCurrGame(e)
      setCurrScore(Array(e.availableParams.length).fill(null))
      return
    }
    setCurrGame(null)
    setCurrScore([null])
  }

  return ReactDOM.createPortal((
    <>
      <div className="modal-page">
        <div className="modal-container">
          <div className="exit-bar">
            <Button onClick={() => props.onClose()} buttonClass="exit-button">x</Button>
          </div>
          <div className="title">Add Score</div>
          {
            options.length &&
            <>
              <div className="entry-line">
                Game:
                <Select options={options} onChange={(newValue) => {updateGame(newValue)}} isSearchable isClearable className="game-menu" />
              </div>
              {currGame && 
                currGame?.availableParams.map((param: Param, idx: number) => {
                  return(
                    <div className="entry-line" key={param.name}>
                      {param.name + ': '}
                      <FluidInput type="number" id="param" min={0} value={currScore[idx]} setValue={(e: number | null) => updateScore(e, idx)} />
                    </div>
                  )
                })
              }
              {
                scoreError &&
                <div>Error: Unable to Submit Score</div>
              }
              <Button onClick={onSubmit} buttonClass="submit-button">Submit Score</Button>
            </>
          }
        </div>
      </div>
    </>
  ), document.getElementById('root') || document.createElement('div'))
}

export default ScoreModal