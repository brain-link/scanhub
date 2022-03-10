import React from "react"


export type ErrorBoundaryProps = {

}

type State = {
  error: Error | null
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, State> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error: Error) {
    return { error }
  }

  componentDidCatch(error: Error, errorInfo: any) {
    // console.log(error, errorInfo)
  }

  render() {
    if (this.state.error !== null) {
      return <div>
        <h1>Error occured</h1>
        <p>{this.state.error.message}</p>
      </div>
    }

    return this.props.children;
  }
}