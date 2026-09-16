const INGESTION_API_URL = import.meta.env.VITE_INGESTION_API_URL;
const AI_REASONING_API_URL = import.meta.env.VITE_AI_REASONING_API_URL;

export interface Alert {
    id: number;
    rule_name: string,
    source_ip: string | null,
    detail: string,
    detected_at: string,
}

export async function fetchAlerts(): Promise<Alert[]> {
    const response = await fetch(`${INGESTION_API_URL}/alerts`);
    if (!response.ok) throw new Error(`Failed to fetch alerts: ${response.status}`);
    return response.json();
}

export async function explainAlert(id: number): Promise<string> {
    const response = await fetch(`${AI_REASONING_API_URL}/explain/${id}`);
    if (!response.ok) throw new Error(`Failed to fetch explanation for alert ${id}: ${response.status}`);
    const data = await response.json();
    return data.explanation;
}