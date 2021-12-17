from sklearn.preprocessing import MinMaxScaler

class UtilityAnalyzer:

    def utility_function(self, data, threshold = 0.04, penality = 1, roof = 3, min_val = 2):
        #print(data[:10])
        _result = []
        for val in data:
            if val >= threshold:
                _result.append((threshold - val))
            else:
                _result.append((threshold - val) * penality)
        #print(_result[:10])
        #print("OLD DATA", _result[-5:])
        #print("MIN VALUE", min(_result))
        #return _result
        _result_ = [float(i) + min_val for i in _result]

        normalized = [float(i)/roof for i in _result_]
        #print("NORMALIZED DATA", normalized[-5:])
        #return normalized
        return normalized

    def cumulate_data(self, data):
        _result, act_sum = [], 0
        for idx, val in enumerate(data):
            if idx == 0:
                _result.append(data[0])
                act_sum = data[0]
            else:
                #print(act_sum)
                _result.append(act_sum + val)
                act_sum += val
        #return _result
        #print("OLD DATA", _result[-5:])
        #scaler = MinMaxScaler()
        #scaler.fit(_result)
        #normalized = scaler.transform(_result)
        #normalized = [float(i)/_result[-1] for i in _result]
        #print("NORMALIZED DATA", normalized[-5:])
        #return normalized
        return _result

    def reverse(self, data):
        _reversed = [1 - item for item in data]
        return _reversed