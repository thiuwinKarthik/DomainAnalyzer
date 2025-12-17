class GraphBuilder:
    def build_graph(self, profile: dict):
        domain = profile.get("domain", "unknown")
        nodes = []
        edges = []

        # 1. Central Node (Company)
        nodes.append({"id": domain, "label": profile.get("company_name", domain), "group": "Company"})

        # 2. Industry Node
        industry = profile.get("industry")
        if industry:
            nodes.append({"id": industry, "label": industry, "group": "Industry"})
            edges.append({"source": domain, "target": industry, "label": "OPERATES_IN"})

        # 3. Product Nodes
        for prod in profile.get("products_services", []):
            nodes.append({"id": prod, "label": prod, "group": "Product"})
            edges.append({"source": domain, "target": prod, "label": "OFFERS"})

        # 4. Tech Stack Nodes
        for tech in profile.get("tech_stack", []):
            nodes.append({"id": tech, "label": tech, "group": "Technology"})
            edges.append({"source": domain, "target": tech, "label": "USES"})

        return {"nodes": nodes, "edges": edges}