import React, { useState } from 'react'

type Props = {
  type: React.HTMLInputTypeAttribute
  label?: string
  id: string
  min?: number
  value: string | number | null
  setValue: Function
}

function FluidInput(props: Props) {
  const [isFocused, setFocused] = useState<boolean>(false)

  let inputClass = "fluid-input"
  if (isFocused) {
    inputClass += " fluid-input--focus"
  } else if (props.value !== "") {
    inputClass += " fluid-input--open"
  }

  return (
    <div className={inputClass} >
      <div className="fluid-input-holder">
        <input
          className="fluid-input-input"
          type={props.type}
          id={props.id}
          min={props.min}
          onFocus={() => setFocused(!isFocused)}
          onBlur={() => setFocused(!isFocused)}
          onChange={(e: React.FormEvent<HTMLInputElement>) => props.setValue(e.currentTarget.value)}
          autoComplete="off"
        />
        <label className="fluid-input-label" id={props.id}>{props.label}</label>
      </div>
    </div>
  )
}

export default FluidInput