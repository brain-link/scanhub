type Props = {
  recordingId: string
}

export function ConfigureMRIModality({
  recordingId,
}: Props) {
  return (
    <>
      Configure MRI ({recordingId})
      <form>
        <label>
          <input></input>
        </label>
        <label>
          <input></input>
        </label>
        <label>
          <input></input>
        </label>
        <label>
          <input></input>
        </label>
        <label>
          <input></input>
        </label>
        <label>
          <input></input>
        </label>
      </form>
    </>
  )
}
