package middlewares

import (
	"context"
	"study_flask_api/utils/loggers"
	"time"

	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"google.golang.org/grpc/peer"
)

func GrpcLogger() grpc.UnaryServerInterceptor {
	return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp interface{}, err error) {
		startTime := time.Now()
		defer func() {
			clientIP := ""
			remoteCon, ok := peer.FromContext(ctx)
			if ok && remoteCon != nil && remoteCon.Addr != nil {
				clientIP = remoteCon.Addr.String()
			}

			log := loggers.GetLogger()
			if err != nil {
				log.WithFields(logrus.Fields{
					"client_ip":    clientIP,
					"req_method":   info.FullMethod,
					"req_string":   req,
					"error":        err.Error(),
					"latency_time": time.Since(startTime),
				}).Error()
			} else {
				log.WithFields(logrus.Fields{
					"client_ip":    clientIP,
					"req_method":   info.FullMethod,
					"req_string":   req,
					"res_string":   resp,
					"latency_time": time.Since(startTime),
				}).Info()
			}
		}()
		resp, err = handler(ctx, req)
		return resp, err
	}
}
