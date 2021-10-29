import React from 'react'

type Props = {
  buttonClass?: string
  onClick?: React.MouseEventHandler<HTMLElement>
}

function Button(props: React.PropsWithChildren<Props>) {
  return (
    <div className={`button ${props.buttonClass}`} onClick={props.onClick}>
      {props.children}
    </div>
  )
}

export default Button
