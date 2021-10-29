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

function ScoreModal(props: Props) {
  const appContext = React.useContext(AppContext)
  const [options, setOptions] = useState<GameDetails[]>([])
  const [currGame, setCurrGame] = useState<string>('')
  const [currScore, setCurrScore] = useState<number | null>(null)
  const [scoreError, setScoreError] = useState<boolean>(false)

  useEffect(() => {
    async function getOptions() {
      const options = await appContext?.backend.getGames()
      setOptions(options)
    }
    getOptions()
  }, [appContext?.backend])

  async function onSubmit() {
    if (currScore && currGame !== '') {
      const result = await appContext?.backend.submitScore(currGame, currScore, appContext.currUser)
      if (result.success) {
        setScoreError(false)
        props.onClose()
      }
    }
    setScoreError(true)
  }

  function assertIsGameDetails(data: unknown): data is GameDetails {
    if (!data) {
      return false
    }
    return (typeof data === 'object') && ('label' in (data as any) && typeof (data as any)['label'] === 'string') &&
    ('value' in (data as any) && typeof (data as any)['value'] === 'number')
  }

  function updateGame(e: unknown) {
    if (assertIsGameDetails(e)) {
      setCurrGame(e.value)
    }
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
              <div className="entry-line">
                Score:
                <FluidInput type="number" id="score" min={0} value={currScore} setValue={setCurrScore} />
              </div>
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