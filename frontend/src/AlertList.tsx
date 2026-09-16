import useSWR from "swr";
import { fetchAlerts } from "./api";
import { AlertRow } from "./AlertRow";
import "./AlertList.css"

export function AlertList() {
  const {
    data: alerts,
    error,
    isLoading,
  } = useSWR("alerts", fetchAlerts, {
    refreshInterval: 5000,
  });

  if (isLoading) return <p>Loading ALerts...</p>;
  if (error) return <p>Failed to load alerts.</p>;

  return (
    <table className="alerts-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Rule</th>
          <th>Source IP</th>
          <th>Detail</th>
          <th>Detected At</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {alerts?.map((alert) => (
          <AlertRow key={alert.id} alert={alert} />
        ))}
      </tbody>
    </table>
  );
}
