export type ResourceGroupName =
  | 'deployments'
  | 'replicaSets'
  | 'pods'
  | 'services'
  | 'experiments'

export type ResourceKindName =
  | 'deployment'
  | 'replicaset'
  | 'pod'
  | 'service'
  | 'experiment'

export interface HealthBlock {
  status: string
  message?: string
}

export interface ClusterStatus {
  clusterName: string
  namespace: string
  provider: string
  mode: string
  scopeLocked: boolean
  controlPlane: HealthBlock
  workload: HealthBlock
  chaosMesh: HealthBlock
}

export interface ResourceRecord {
  kind: string
  name: string
  status?: string
  updatedAt?: string | null
  [key: string]: unknown
}

export interface ClusterEventRecord {
  name?: string
  type?: string
  reason?: string
  message?: string
  resourceKind?: string
  resourceName?: string
  timestamp?: string | null
}

export interface ResourceSnapshot {
  mode: string
  namespace: string
  resources: Record<ResourceGroupName, ResourceRecord[]>
  events: ClusterEventRecord[]
}

export interface ClusterSnapshotEvent {
  status: ClusterStatus
  resources: ResourceSnapshot
}
