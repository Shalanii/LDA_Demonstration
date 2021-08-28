class Measures:
    def nmi(self,doc2clust, doc2cat):
        import math

        dict1 = {}
        dict2 = {}
        num = 0.0
        den_gs = 0.0
        den_my = 0.0

        for l in range(0,len(doc2clust)):
            if doc2clust[l][0] not in dict1:
                dict1[doc2clust[l][0]] = set([])
            dict1[doc2clust[l][0]].add(int(l))

        for l in range(0,len(doc2clust)):
            if doc2cat[l][0] not in dict2:
                dict2[doc2cat[l][0]] = set([])
            dict2[doc2cat[l][0]].add(int(l))

        for event_my in dict1:
            den_gs += (float(len(dict1[event_my])) / float(len(doc2cat))) * math.log(
                float(len(dict1[event_my])) / float(len(doc2cat)), 2)
            eset = set()
            for entry in dict1[event_my]:
                for en in doc2cat[entry]:
                    eset.add(en)
            for event_gs in eset:
                num += (float(len(dict1[event_my] & dict2[event_gs])) / float(len(doc2cat))) * (math.log(
                    (float(len(doc2cat)) * float(len(dict1[event_my] & dict2[event_gs]))) / (
                                float(len(dict1[event_my])) * float(len(dict2[event_gs]))), 2))

        for event_gs in dict2:
            den_my += float(len(dict2[event_gs])) / float(len(doc2cat)) * math.log(
                float(len(dict2[event_gs])) / float(len(doc2cat)), 2)

        nmi = num / (((-1) * den_gs + (-1) * den_my) / 2)

        return nmi
     
    def microf1(self,doc2clust, doc2cat):
        dict1 = {}; dict2 = {}; prec = 0.0; rec = 0.0
        for l in doc2clust:
            if doc2clust[l][0] not in dict1:
                dict1[doc2clust[l][0]] = set([])
            dict1[doc2clust[l][0]].add(int(l))
     
        for l in doc2cat:
            if doc2cat[l][0] not in dict2:
                dict2[doc2cat[l][0]] = set([])
            dict2[doc2cat[l][0]].add(int(l))
     
        for doc in doc2cat:
            prec += ( float(len(dict1[doc2clust[doc][0]] & dict2[doc2cat[doc][0]])) / float(len(dict1[doc2clust[doc][0]])) )
            rec  += ( float(len(dict1[doc2clust[doc][0]] & dict2[doc2cat[doc][0]])) / float(len(dict2[doc2cat[doc][0]])) )
     
        prec = prec / float(len(doc2cat))
        rec = rec / float(len(doc2cat))
        fmeasure = 2.0 * prec * rec / (prec + rec)
     
        return fmeasure
     
    def clust_distribution(self,clust2size):
        import math
        sizes = clust2size.values()
        cMean = float(sum(sizes)) / len(sizes)
        diff_mean_squared = [(float(x) - cMean)**2 for x in sizes]
        observations = len(sizes)
        cStdDev = math.sqrt(sum(diff_mean_squared) / float(observations))
        cMax=max(sizes)
        cMin=min(sizes)
        return cMean,cStdDev,cMax,cMin
     
    def load(self,dclass,dclust):
        doc2clust = {}
        doc2cat = {}
        original_clust2size = {}
        doc2cat = dict((i,[doc]) for i,doc in enumerate(dclass));all_categories = set([c[0] for c in doc2cat.values()])
        doc2clust = dict((i,[doc]) for i,doc in enumerate(dclust));all_clusters = set([c[0] for c in doc2clust.values()])
     
        for cluster, docs in self.invert(doc2clust).items():
            original_clust2size[cluster] = len(docs)
        cMean,cStdDev,cMax,cMin=self.clust_distribution(original_clust2size)
     
        return (doc2clust, doc2cat, len(all_clusters), len(all_categories),cMean,cStdDev,cMax,cMin)
     
    def invert(self,key2values):
        value2keys = {}
        for key, values in key2values.items():
            for value in values:
                if value in value2keys:
                    value2keys[value].append(key)
                else:
                    value2keys[value] = [key]
        return value2keys
     
    def f1_nmi(self,dclass,dclust):
        doc2clust, doc2cat, cluster_count,class_count,cMean,cStdDev,cMax,cMin = self.load(dclass,dclust)
        df1 = self.microf1(doc2clust, doc2cat)
        dnmi = self.nmi(doc2clust, doc2cat)
        return df1,dnmi,cluster_count,class_count,cMean,cStdDev,cMax,cMin
        
   

