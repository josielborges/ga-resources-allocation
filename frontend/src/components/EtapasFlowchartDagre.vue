<template>
  <div class="flowchart-container">
    <div class="flowchart-header">
      <h5 class="text-sm font-medium text-gray-700 mb-2">Fluxograma das Etapas</h5>
    </div>
    <div ref="flowchart" class="flowchart-svg-container border border-gray-200 rounded bg-gray-50 min-h-[150px]"></div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import dagre from 'dagre'

export default {
  name: 'EtapasFlowchartDagre',
  props: {
    etapas: {
      type: Array,
      default: () => []
    }
  },
  watch: {
    etapas: {
      handler() {
        this.renderFlowchart()
      },
      deep: true
    }
  },
  mounted() {
    this.renderFlowchart()
  },
  methods: {
    renderFlowchart() {
      if (!this.etapas || this.etapas.length === 0) {
        d3.select(this.$refs.flowchart).selectAll('*').remove()
        return
      }

      const container = d3.select(this.$refs.flowchart)
      container.selectAll('*').remove()

      // Create dagre graph
      const g = new dagre.graphlib.Graph()
      g.setGraph({ rankdir: 'LR', nodesep: 15, ranksep: 40 })
      g.setDefaultEdgeLabel(() => ({}))

      // Create temporary SVG for text measurement
      const tempSvg = container.append('svg').style('visibility', 'hidden')
      const tempText = tempSvg.append('text')
        .attr('font-size', '11px')
        .attr('font-family', 'Inter, -apple-system, BlinkMacSystemFont, sans-serif')

      // Add nodes to graph with dynamic sizing
      this.etapas.forEach((etapa, index) => {
        const nodeId = index.toString()
        const label = etapa.nome || `Etapa ${index + 1}`
        
        // Measure text width
        tempText.text(label)
        const textWidth = tempText.node().getBBox().width
        const numberWidth = 18 // Fixed width for number section
        const nodeWidth = Math.max(80, textWidth + numberWidth + 16)
        
        g.setNode(nodeId, {
          label: label,
          width: nodeWidth,
          height: 30,
          index: index,
          numberWidth: numberWidth
        })
      })
      
      // Remove temporary SVG
      tempSvg.remove()

      // Add edges based on predecessors
      this.etapas.forEach((etapa, index) => {
        if (etapa.predecessoras && etapa.predecessoras.length > 0) {
          etapa.predecessoras.forEach(predIndex => {
            if (predIndex < this.etapas.length) {
              g.setEdge(predIndex.toString(), index.toString())
            }
          })
        }
      })

      // Layout the graph
      dagre.layout(g)

      // Get graph dimensions and container size
      const graphWidth = g.graph().width
      const graphHeight = g.graph().height
      const containerWidth = this.$refs.flowchart.clientWidth
      const padding = 10
      const containerHeight = Math.max(120, graphHeight + padding * 2)
      
      // Adjust div height
      this.$refs.flowchart.style.height = `${containerHeight}px`
      
      // Calculate centering offsets
      const offsetX = Math.max(padding, (containerWidth - graphWidth) / 2)
      const offsetY = Math.max(padding, (containerHeight - graphHeight) / 2)

      // Create SVG
      const svg = container
        .append('svg')
        .attr('width', containerWidth)
        .attr('height', containerHeight)

      const svgGroup = svg.append('g')
        .attr('transform', `translate(${offsetX}, ${offsetY})`)

      // Add arrow marker
      svg.append('defs')
        .append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 8)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('fill', '#6b7280')

      // Draw edges
      g.edges().forEach(e => {
        const edge = g.edge(e)
        const line = d3.line()
          .x(d => d.x)
          .y(d => d.y)
          .curve(d3.curveMonotoneX)

        svgGroup.append('path')
          .attr('d', line(edge.points))
          .attr('stroke', '#6b7280')
          .attr('stroke-width', 2)
          .attr('fill', 'none')
          .attr('marker-end', 'url(#arrowhead)')
      })

      // Draw nodes
      g.nodes().forEach(nodeId => {
        const node = g.node(nodeId)
        const nodeGroup = svgGroup.append('g')
          .attr('transform', `translate(${node.x - node.width/2}, ${node.y - node.height/2})`)

        // Main balloon outline
        nodeGroup.append('rect')
          .attr('width', node.width)
          .attr('height', node.height)
          .attr('rx', 4)
          .attr('fill', '#f9fafb')
          .attr('stroke', '#e5e7eb')
          .attr('stroke-width', 1)

        // Number section with rounded left corners only
        nodeGroup.append('path')
          .attr('d', `M 4,0 A 4,4 0 0,0 0,4 L 0,${node.height-4} A 4,4 0 0,0 4,${node.height} L ${node.numberWidth},${node.height} L ${node.numberWidth},0 Z`)
          .attr('fill', '#3b82f6')

        // Separator line
        nodeGroup.append('line')
          .attr('x1', node.numberWidth)
          .attr('y1', 0)
          .attr('x2', node.numberWidth)
          .attr('y2', node.height)
          .attr('stroke', '#e5e7eb')
          .attr('stroke-width', 1)

        // Node label (description)
        nodeGroup.append('text')
          .attr('x', node.numberWidth + (node.width - node.numberWidth) / 2)
          .attr('y', node.height / 2)
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('fill', '#374151')
          .attr('font-size', '11px')
          .attr('font-weight', '500')
          .attr('font-family', 'Inter, -apple-system, BlinkMacSystemFont, sans-serif')
          .text(node.label)

        // Node number (inside blue section)
        nodeGroup.append('text')
          .attr('x', node.numberWidth / 2)
          .attr('y', node.height / 2)
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('fill', 'white')
          .attr('font-size', '10px')
          .attr('font-weight', '600')
          .attr('font-family', 'Inter, -apple-system, BlinkMacSystemFont, sans-serif')
          .text(node.index + 1)
      })
    }
  }
}
</script>

<style scoped>
.flowchart-container {
  margin-top: 16px;
}

.flowchart-svg-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>