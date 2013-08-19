root = exports ? this

zoom = d3.behavior.zoom()

# Help with the placement of nodes
RadialPlacement = () ->
  # stores the key -> location values
  values = d3.map()
  # how much to separate each location by
  increment = 20
  # how large to make the layout
  radius = 200
  # where the center of the layout should be
  center = {"x":0, "y":0}
  # what angle to start at
  start = -120
  current = start

  # Given an center point, angle, and radius length,
  # return a radial position for that angle
  radialLocation = (center, angle, radius) ->
    x = (center.x + radius * Math.cos(angle * Math.PI / 180))
    y = (center.y + radius * Math.sin(angle * Math.PI / 180))
    {"x":x,"y":y}

  # Main entry point for RadialPlacement
  # Returns location for a particular key,
  # creating a new location if necessary.
  placement = (key) ->
    value = values.get(key)
    if !values.has(key)
      value = place(key)
    value

  # Gets a new location for input key
  place = (key) ->
    value = radialLocation(center, current, radius)
    values.set(key,value)
    current += increment
    value

  # Given a set of keys, perform some
  # magic to create a two ringed radial layout.
  # Expects radius, increment, and center to be set.
  # If there are a small number of keys, just make
  # one circle.
  setKeys = (keys) ->
    # start with an empty values
    values = d3.map()

    # number of keys to go in first circle
    firstCircleCount = 360 / increment

    # if we don't have enough keys, modify increment
    # so that they all fit in one circle
    if keys.length < firstCircleCount
      increment = 360 / keys.length

    # set locations for inner circle
    firstCircleKeys = keys.slice(0,firstCircleCount)
    firstCircleKeys.forEach (k) -> place(k)

    # set locations for outer circle
    secondCircleKeys = keys.slice(firstCircleCount)

    # setup outer circle
    radius = radius + radius / 1.8
    increment = 360 / secondCircleKeys.length

    secondCircleKeys.forEach (k) -> place(k)

  placement.keys = (_) ->
    if !arguments.length
      return d3.keys(values)
    setKeys(_)
    placement

  placement.center = (_) ->
    if !arguments.length
      return center
    center = _
    placement

  placement.radius = (_) ->
    if !arguments.length
      return radius
    radius = _
    placement

  placement.start = (_) ->
    if !arguments.length
      return start
    start = _
    current = start
    placement

  placement.increment = (_) ->
    if !arguments.length
      return increment
    increment = _
    placement

  return placement

Network = () ->
  # variables we want to access
  # in multiple places of Network
  width = widthW
  height = heightW
  # allData will store the unfiltered data
  allData = []
  dataJson = []
  curLinksData = []
  curNodesData = []
  linkedByIndex = {}
  # these will hold the svg groups for
  # accessing the nodes and links display
  nodesG = null
  linksG = null
  textG = null
  # these will point to the circles and lines
  # of the nodes and links
  node = null
  link = null
  text = null
  textNode = null
  # variables to refect the current settings
  # of the visualization
  layout = "force"
  filter = "all"
  sort = "songs"
  group = "all"
  # groupCenters will store our radial layout for
  # the group by artist layout.
  groupCenters = null
  vis = null
  lastzoom = 1
  lasttranslate = [0,0]
  zoomb = d3.behavior.zoom()

  # our force directed layout
  force = d3.layout.force()
  # color function used to color nodes
  #nodeColors = d3.scale.category10()
  nodeColors = (x) ->
    group_color = '#ebebeb'
    #group_color = '#ebebeb' if x.indexOf('persona')>=0
    #group_color = '#ff7f0e' if x.indexOf('organizacion')>=0
    #group_color = '#2ca02c' if x.indexOf('empresa')>=0
    group_color
  # tooltip used to display details
  tooltip = Tooltip("vis-tooltip", 450)
  label = Tooltip("vis-label", 100)

  # charge used in artist layout
  charge = (node) -> -Math.pow(node.radius, 2.0) / 2

  # Starting point for network visualization
  # Initializes visualization and starts force layout
  network = (selection, data) ->
    # format our data
    dataJson = data
    allData = setupData(data)

    # create our svg and groups
    vis = d3.select(selection).append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .call(zoomb.scaleExtent([0.5, 8]).on("zoom", zoom))
      .append("g")

    linksG = vis.append("g").attr("id", "links")
    nodesG = vis.append("g").attr("id", "nodes")
    textG = vis.append("g").attr("id","textos")

    # setup the size of the force environment
    force.size([width, height])
    setGroup("all")
    setLayout("force")
    setFilter("all")

    # perform rendering and start force layout
    update()



  # The update() function performs the bulk of the
  # work to setup our visualization based on the
  # current layout/sort/filter.
  #
  # update() is called everytime a parameter changes
  # and the network needs to be reset.
  update = () ->
    # filter data to show based on current filter settings.
    if group == "all"
      curNodesData = filterNodes(allData.nodes)
      curLinksData = filterLinks(allData.links, curNodesData)

    else
      curLinksData = filterLinksGroup(allData.links)
      curNodesData = filterNodestoLinks(curLinksData,allData.nodes)
      console.log(curNodesData)
    # sort nodes based on current sort and update centers for
    # radial layout
    if layout == "radial"
      groups = sortedGroups(curNodesData, curLinksData)
      updateCenters(groups)

    # reset nodes in force layout
    force.nodes(curNodesData)

    # enter / exit for nodes
    updateText()
    updateNodes()


    # always show links in force layout
    if layout == "force"
      force.links(curLinksData)
      updateLinks()
    else
      # reset links so they do not interfere with
      # other layouts. updateLinks() will be called when
      # force is done animating.
      force.links([])
      # if present, remove them from svg 
      if link
        link.data([]).exit().remove()
        link = null

    # start me up!
    force.start()

  # Public function to switch between layouts
  network.restoreData = (newData) ->
    network.toggleGroup('all')
    d3.json mapaURL, (data) ->
      network.updateData(data)


  # Public function to switch between layouts
  network.toggleLayout = (newLayout) ->
    force.stop()
    setLayout(newLayout)
    update()

  # Public function to switch between filter options
  network.toggleFilter = (newFilter) ->
    force.stop()
    setFilter(newFilter)
    update()

  # Public function to switch between sort options
  network.toggleSort = (newSort) ->
    force.stop()
    setSort(newSort)
    update()

  # Public function to switch between group options
  network.toggleGroup = (newGroup) ->
    console.log(newGroup+'inside Toggle')
    force.stop()
    setGroup(newGroup)
    update()

  # Public function to update highlighted nodes
  # from search
  network.updateSearch = (searchTerm) ->
    searchRegEx = new RegExp(searchTerm.toLowerCase())
    node.each (d) ->
      element = d3.select(this)
      match = d.name.toLowerCase().search(searchRegEx)
      if searchTerm.length > 0 and match >= 0
        element.style("fill", "#FF0000")
          .style("stroke-width", 2.0)
          .style("stroke", "#555")
          .attr("r", (d) -> 10)
        #showDetails(d)

        d.searched = true
      else
        d.searched = false
        element.style("fill", (d) -> nodeColors(d.group))
          .style("stroke-width", 1.0)
          .attr("r", (d) -> d.radius)
        #hideDetails(d)

  network.updateData = (newData) ->
    allData = setupData(newData)
    link.remove()
    #node.remove()
    #text.remove()
    #textNode.remove()
    update()

  # called once to clean up raw data and switch links to
  # point to node instances
  # Returns modified data
  setupData = (data) ->
    # initialize circle radius scale
    countExtent = d3.extent(data.nodes, (d) -> d.relevance)
    circleRadius = d3.scale.sqrt().range([11, 12]).domain(countExtent)

    d3.select("#groups").html("<h3><br></h3>Filtrar por conexión:")
    values=['all']
    data.links.forEach (l) ->
      if values.indexOf(l.grupo)==-1
          values.push(l.grupo)
      values

    console.log(values)

    d3.select(".zoom-in").on("click",zoom_in)
    d3.select(".zoom-out").on("click",zoom_out)
    d3.select(".zoom-reset").on("click",zoom_reset)

    d3.select("#groups").append("select")
      .on("change", change)
      .selectAll("option").data(values).enter()
      .append("option")
      .attr("value", (d) -> d)
      .text( (d) -> d )

    data.nodes.forEach (n) ->
      # set initial x/y to values within the width/height
      # of the visualization
      n.x = randomnumber=Math.floor(Math.random()*width)
      n.y = randomnumber=Math.floor(Math.random()*height)
      # add radius to the node so we can use it later
      n.radius = circleRadius(n.relevance)

    # id's -> node objects
    nodesMap  = mapNodes(data.nodes)

    # switch links to point to node objects instead of id's
    data.links.forEach (l) ->
      l.source = nodesMap.get(l.source)
      l.target = nodesMap.get(l.target)

      # linkedByIndex is used for link sorting
      linkedByIndex["#{l.source.id},#{l.target.id}"] = 1

    data

  # Helper function to map node id's to node objects.
  # Returns d3.map of ids -> nodes
  mapNodes = (nodes) ->
    nodesMap = d3.map()
    nodes.forEach (n) ->
      nodesMap.set(n.id, n)
    nodesMap

  # Helper function that returns an associative array
  # with counts of unique attr in nodes
  # attr is value stored in node, like 'artist'
  nodeCounts = (nodes, attr) ->
    counts = {}
    nodes.forEach (d) ->
      counts[d[attr]] ?= 0
      counts[d[attr]] += 1
    counts

  # Given two nodes a and b, returns true if
  # there is a link between them.
  # Uses linkedByIndex initialized in setupData
  neighboring = (a, b) ->
    linkedByIndex[a.id + "," + b.id] or
    linkedByIndex[b.id + "," + a.id]

  # Removes links from input array
  # based on current filter setting.
  # Returns array of links
  filterLinksGroup = (allLinks) ->
    filteredLinks = allLinks
    if group != 'all'
      console.log(group)
      filteredLinks = allLinks.filter (l) -> l.grupo == group
      console.log(filteredLinks)
    filteredLinks


  # Removes nodes from input array
  # based on current filter setting.
  # Returns array of nodes
  filterNodes = (allNodes) ->
    filteredNodes = allNodes
    #if filter == "relevante" or filter == "menor"
    #  relevances = allNodes.map((d) -> d.relevance).sort(d3.ascending)
    #  cutoff = d3.quantile(relevances, 0.5)
    #  filteredNodes = allNodes.filter (n) ->
    #    if filter == "relevante"
    #      n.relevance > cutoff
    #    else if filter == "menor"
    #      n.relevance <= cutoff

    filteredNodes

  # Returns array of Entity (Groups) sorted based on
  # current sorting method.
  sortedGroups = (nodes,links) ->
    groups = []
    if sort == "links"
      counts = {}
      links.forEach (l) ->
        counts[l.source.group] ?= 0
        counts[l.source.group] += 1
        counts[l.target.group] ?= 0
        counts[l.target.group] += 1
      # add any missing groups that dont have any links
      nodes.forEach (n) ->
        counts[n.group] ?= 0

      # sort based on counts
      groups = d3.entries(counts).sort (a,b) ->
        b.value - a.value
      # get just names
      groups = groups.map (v) -> v.key
    else
      # sort groups by song count
      counts = nodeCounts(nodes, "group")
      groups = d3.entries(counts).sort (a,b) ->
        b.value - a.value
      groups = groups.map (v) -> v.key

    groups

  updateCenters = (groups) ->
    if layout == "radial"
      groupCenters = RadialPlacement().center({"x":width/2, "y":height / 2 - 100})
        .radius(300).increment(18).keys(groups)

  filterNewNodes = (newNodes, allNodes) ->
    curNodes = mapNodes(allNodes)
    filteredNodes=newNodes.filter (n) ->
      not (curNodes.get(n.id) or 0)
    filteredNodes


  # Removes nodes from allNodes whose
  # source or target is not present in curLinks
  # Returns array of nodes
  filterNodestoLinks = (curLinks, allNodes) ->
    console.log(allNodes)
    curNodes = mapNodes(allNodes)
    filterNodes2links=allNodes.filter (n) ->
      nodeinLinks(n,curLinks)
      ##  console.log(n.id+":"+l.source.id + "->"+l.target.id)
      #(n.id == l.source.id) or (n.id == l.target.id)
      ##curNodes.get(l.source.id) or curNodes.get(l.target.id)

    filterNodes2links

  nodeinLinks = (node, allLinks) ->
    result = false
    allLinks.forEach (l) ->
      result_tmp = (node.id == l.source.id) or (node.id == l.target.id)
      if result_tmp == true
        result = true
    result

  filterNewLinks = (newLinks, allNodes) ->
    newnodes= mapNodes(allNodes)
    newLinks.filter (l) ->
      newnodes.get(l.source) and newnodes(l.target)

  # Removes links from allLinks whose
  # source or target is not present in curNodes
  # Returns array of links
  filterLinks = (allLinks, curNodes) ->
    curNodes = mapNodes(curNodes)
    allLinks.filter (l) ->
      curNodes.get(l.source.id) and curNodes.get(l.target.id)

  updateText = () ->
    text = textG.selectAll("g")
      .data(curNodesData, (d) -> d.id)

    textNode = text.enter().append("g")
      .attr("transform", (d) -> "translate(" + d.x + "," + d.y  + ")")

    textNode
      .append("image")
      .attr("xlink:href", (d) -> d.imagen)
      .attr("x", -8)
      .attr("y", -8)
      .attr("width", 32)
      .attr("height", 32)

    #textNode
    #  .append("text")
    #  .attr("x",8)
    #  .attr("y","-.31em")
    #  .attr("class","text")
    #  .text((d)->d.name)

    text.on("mouseover", showLabel)
      .on("mouseout", hideLabel)


    text.on("dblclick", loadJson)
    text.on("click", showDetails)

    text.exit().remove()



  # enter/exit display for nodes
  updateNodes = () ->
    node = nodesG.selectAll("circle.node")
      .data(curNodesData, (d) -> d.id)

    node.enter().append("circle")
      .attr("class", "node")
      .attr("cx", (d) -> d.x)
      .attr("cy", (d) -> d.y)
      .attr("r", (d) -> d.radius)
      .style("fill", (d) -> nodeColors(d.group))
      .style("stroke", (d) -> strokeFor(d))
      .style("stroke-width", 1.0)

    #node.on("mouseover", showDetails)
    #  .on("mouseout", hideDetails)

    #node.on("click",loadJson)


    node.exit().remove()

  # enter/exit display for links
  updateLinks = () ->
    link = linksG.selectAll("line.link")
      .data(curLinksData, (d) -> "#{d.source.id}_#{d.target.id}")
    link.enter().append("line")
      .attr("class", "link")
      .attr("stroke", "#ddd")
      .attr("stroke-opacity", 0.8)
      .attr("x1", (d) -> d.source.x)
      .attr("y1", (d) -> d.source.y)
      .attr("x2", (d) -> d.target.x)
      .attr("y2", (d) -> d.target.y)


    link.exit().remove()

  # switches force to new layout parameters
  setLayout = (newLayout) ->
    layout = newLayout
    if layout == "force"
      force.on("tick", forceTick)
        .charge(-280)
        .linkDistance(250)
    else if layout == "radial"
      force.on("tick", radialTick)
        .charge(charge)

  # switches filter option to new filter
  setFilter = (newFilter) ->
    filter = newFilter

  # switches sort option to new sort
  setSort = (newSort) ->
    sort = newSort

  # switches group option to new group
  setGroup = (newGroup) ->
    console.log(newGroup+'insede Set')
    group = newGroup

  # tick function for force directed layout
  forceTick = (e) ->

    text
      .attr("transform", (d) -> "translate(" + d.x + "," + d.y  + ")")
    #    dx = (d.target.x - d.source.x)
    #    dy = (d.target.y - d.source.y)
    #    dr = Math.sqrt(dx * dx + dy * dy)
    #    sinus = dy/dr
    #    cosinus = dx/dr
    #    l = d.grupo.length*6
    #    offset = (1 - (l / dr )) / 2
    #    x=(d.source.x + dx*offset)
    #    y=(d.source.y + dy*offset)
    #    "translate(" + x + "," + y + ") matrix("+cosinus+", "+sinus+", "+-sinus+", "+cosinus+", 0 , 0)"
    #  )

    node
      .attr("cx", (d) -> d.x)
      .attr("cy", (d) -> d.y)

    link
      .attr("x1", (d) -> d.source.x)
      .attr("y1", (d) -> d.source.y)
      .attr("x2", (d) -> d.target.x)
      .attr("y2", (d) -> d.target.y)

  # tick function for radial layout
  radialTick = (e) ->
    node.each(moveToRadialLayout(e.alpha))

    node
      .attr("cx", (d) -> d.x)
      .attr("cy", (d) -> d.y)

    text
      .attr("transform", (d) -> "translate(" + d.x + "," + d.y  + ")")

    if e.alpha < 0.03
      force.stop()
      updateLinks()

  # Adjusts x/y for each node to
  # push them towards appropriate location.
  # Uses alpha to dampen effect over time.
  moveToRadialLayout = (alpha) ->

    k = alpha * 0.1
    (d) ->
      centerNode = groupCenters(d.group)
      d.x += (centerNode.x - d.x) * k
      d.y += (centerNode.y - d.y) * k


  # Helper function that returns stroke color for
  # particular node.
  strokeFor = (d) ->
    #d3.rgb(nodeColors(d.group)).darker().toString()
    d3.rgb(nodeColors(d.group))

  notinNodes = (node) ->
    isNode = true
    log("node",node.id)
    allData.nodes.forEach (n) ->
      log("n",n.id)
      if n.id == node.id
        isNode = false
    isNode


  loadJson = (d,i) ->
    d3.json '/visualizacion/call/json/childnodes/'+d.id, (data) ->
      log(data.links)
      #newData = setupData(data)
      #log("json",newData.links)
      newNodes = filterNewNodes(data.nodes,allData.nodes)
      #newLinks =  filterLinks(newData.links, allData.links)
      #log("newNodes",newNodes)


      newNodes.forEach (n) ->
        allData.nodes.push(n)

      nodesMap  = mapNodes(allData.nodes)

    # initialize circle radius scale
      countExtent = d3.extent(data.nodes, (d) -> d.relevance)
      circleRadius = d3.scale.sqrt().range([11, 12]).domain(countExtent)

      allData.nodes.forEach (n) ->
        # set initial x/y to values within the width/height
        # of the visualization
        n.x = randomnumber=Math.floor(Math.random()*width)
        n.y = randomnumber=Math.floor(Math.random()*height)
        # add radius to the node so we can use it later
        n.radius = circleRadius(n.relevance)
    # switch links to point to node objects instead of id's
      data.links.forEach (l) ->
        l.source = nodesMap.get(l.source)
        l.target = nodesMap.get(l.target)

        # linkedByIndex is used for link sorting
        linkedByIndex["#{l.source.id},#{l.target.id}"] = 1
      log("links",data.links)
      newData = {'nodes':newNodes,'links':data.links}

      #newData = setupData(newData)
      #log("newData",newData)
      #newData = setupData(data)
      data.links.forEach (l) ->
        allData.links.push(l)
      #log(allData)
      #data.nodes.forEach = (n) ->
      #  nodetmp = {'id':n.id,'name':n.name,'relevance':n.relevance}
      #  curNodesData.push(n)
      #  dataJson.nodes.push(n)

      #data.links.forEach = (l) ->
      #  dataJson.links.push(l)
      #network.updateData(newData)
      update()

  showLabel = (d,i) ->
    content = d.name
    label.showTooltip(content,d3.event)

  hideLabel = (d,i) ->
    label.hideTooltip()

  zoom_in = () ->
    lastzoom = lastzoom * 1.2
    zoomb.scale(1)
    zoomb.translate([width*(1-lastzoom)/2,height*(1-lastzoom)/2])
    vis.transition().duration(500).attr("transform", "translate(" + zoomb.translate() + ")scale(" +lastzoom + ")")
    zoomb.translate(zoomb.translate()).scale(lastzoom)

  zoom_reset = () ->
      zoomb.scale(1)
      zoomb.translate([0,0])
      lastzoom = 1
      vis.transition().duration(500).attr("transform", "translate(" + zoomb.translate() + ")scale(" + "1" + ")")
      zoomb.translate(zoomb.translate()).scale(1)


  zoom_out = () ->
    lastzoom = lastzoom * 0.8
    zoomb.scale(1)
    zoomb.translate([width*(1-lastzoom)/2,height*(1-lastzoom)/2])
    vis.transition().duration(500).attr("transform", "translate(" + zoomb.translate() + ")scale(" +lastzoom + ")")
    zoomb.translate(zoomb.translate()).scale(lastzoom)

  zoom = () ->
    delta = lastzoom - d3.event.scale
    console.log(delta)
    d3.select("#textos").style('cursor', '-moz-grab')
    d3.select("#textos").style('cursor', '-webkit-grab')
    if delta<0
      d3.select("#textos").style('cursor', '-moz-zoom-in')
      d3.select("#textos").style('cursor', '-webkit-zoom-in')
    if delta>0
      d3.select("#textos").style('cursor', '-moz-zoom-out')
      d3.select("#textos").style('cursor', '-webkit-zoom-out')

    lasttranslate = d3.event.translate
    lastzoom= d3.event.scale
    vis.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")")

  # Mouseout function
  hideDetails = (d,i) ->
    tooltip.hideTooltip()
    # watch out - don't mess with node if search is currently matching
    node.style("stroke", (n) -> if !n.searched then strokeFor(n) else "#555")
      .style("stroke-width", (n) -> if !n.searched then 1.0 else 2.0)
    if link
      link.attr("stroke", "#ddd")
        .attr("stroke-opacity", 0.8)

  # Mouseover tooltip function
  showDetails = (d,i) ->
    label.hideTooltip()
    content = '<img src="' + d.imagen + '" class="imagen-perfil-ch" width="140">'
    content += '<h3 class="perfil-name ">' + d.name + ' '
    content += '<a href="#" class="sugest-right" onclick="$(\'div.tooltip\').hide()">x</a></h3>'
    content += '<p class="perfil-details">' + d.shortBio + '</p>  '
    content += '<a href="' + d.url + '" class="sugest-right">Ver Perfil ▶</a>'
    tooltip.showTooltip(content,d3.event)


    # higlight connected links
    if link
      link.attr("stroke", (l) ->
        if l.source == d or l.target == d then "#555" else "#ddd"
      )
        .attr("stroke-opacity", (l) ->
          if l.source == d or l.target == d then 1.0 else 0.5
        )


    # link.each (l) ->
    #   if l.source == d or l.target == d
    #     d3.select(this).attr("stroke", "#555")

    # highlight neighboring nodes
    # watch out - don't mess with node if search is currently matching
    node.style("stroke", (n) ->
      if (n.searched or neighboring(d, n)) then "#555" else strokeFor(n))
      .style("stroke-width", (n) ->
        if (n.searched or neighboring(d, n)) then 2.0 else 1.0)

    # highlight the node being moused over
    d3.select(this).style("stroke","black")
      .style("stroke-width", 2.0)



  change = () ->
    console.log(network)
    newGroup = this.options[this.selectedIndex].value
    network.toggleGroup(newGroup)
    #this.options[this.selectedIndex].value

  # Final act of Network() function is to return the inner 'network()' function.
  return network

# Activate selector button
activate = (group, link) ->
  d3.selectAll("##{group} a").classed("active", false)
  d3.select("##{group} ##{link}").classed("active", true)



$ ->
  myNetwork = Network()

  d3.selectAll("#data a").on "click", (d) ->
    newData = d3.select(this).attr("id")
    activate("data", newData)
    myNetwork.restoreData(newData)

  d3.selectAll("#layouts a").on "click", (d) ->
    newLayout = d3.select(this).attr("id")
    console.log('mauenda '+newLayout)
    activate("layouts", newLayout)
    myNetwork.toggleLayout(newLayout)



  #d3.selectAll("#groups").on "change", (d) ->
    #console.log(d3.select(this).select("option:selected"))
    #newGroup = d3.select(this).selectAll("option:selected").attr("id")
    #myNetwork.toggleGroup(newGroup)

  d3.selectAll("#sorts a").on "click", (d) ->
    newSort = d3.select(this).attr("id")
    activate("sorts", newSort)
    myNetwork.toggleSort(newSort)




  $("#search").keyup () ->
    searchTerm = $(this).val()
    myNetwork.updateSearch(searchTerm)

  d3.json mapaURL, (json) ->
    myNetwork("#vis", json)



