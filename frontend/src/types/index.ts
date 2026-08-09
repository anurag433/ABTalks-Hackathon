export interface PublishedPost {
  id: string;
  title?: string;
  summary?: string;
  technical_deep_dive?: string;
  why_it_matters?: string;
  rationale?: string;
  category?: string;
  keywords?: string[];
  sources?: (string | { name: string; url: string })[];
  editorial_score?: number;
  status?: string;
  published_at?: string;
  createdAt?: string;
  text?: string;
}

export interface RejectedTopic {
  id: string;
  title: string;
  url: string;
  category: string;
  editorial_score: number;
  rejection_reason: string;
  rejected_at: string;
}

export interface MemoryNode {
  memory_id: string;
  post_id: string;
  title: string;
  summary: string;
  created_at: string;
}

export interface AgentStatusData {
  agent_id?: string;
  persona_name?: string;
  persona_domain?: string;
  current_phase: string;
  last_run_at: string | null;
  next_run_at: string | null;
  total_discovered: number;
  total_published: number;
  total_rejected: number;
  is_initialized: boolean;
  started_at: string;
  status_message: string;
}

export interface GraphNode {
  id: string;
  label: string;
  full_title: string;
  category: string;
  created_at: string | null;
  post_id: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  weight: number;
}

export interface KnowledgeGraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  total_nodes: number;
  total_edges: number;
}
