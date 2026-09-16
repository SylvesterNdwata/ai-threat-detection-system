import { useState } from "react";
import { explainAlert, type Alert } from "./api";
import { SparkleIcon } from "./SparkleIcon";

export function AlertRow({ alert }: { alert: Alert }) {
  const [explanation, setExplanation] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleExplain() {
    setLoading(true);
    setError(null);
    try {
      setExplanation(await explainAlert(alert.id));
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to get explanation",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <tr>
        <td>{alert.id}</td>
        <td>{alert.rule_name}</td>
        <td>{alert.source_ip ?? "N/A"}</td>
        <td>{alert.detail}</td>
        <td>{alert.detected_at}</td>
        <td>
          <button onClick={handleExplain} disabled={loading}>
            <SparkleIcon />
            {loading ? "Explaining..." : "Explain"}
          </button>
        </td>
      </tr>
      {explanation !== null ? (
        <tr>
          <td colSpan={6}>{explanation}</td>
        </tr>
      ) : null}
      {error !== null ? (
        <tr>
          <td colSpan={6} style={{ color: "red" }}>
            {error}
          </td>
        </tr>
      ) : null}
    </>
  );
}
